import pulumi
import pulumi_cloudflare as cloudflare
from pathlib import Path

config = pulumi.Config("rnp")
zone = config.require_secret("zone_id")
account_id = config.require_secret("account_id")

# Read Hugo version from .hugo-version file
hugo_version_file = Path(__file__).parent.parent / ".hugo-version"
HUGO_VERSION = hugo_version_file.read_text().strip()

# Read Go version from .go-version file
go_version_file = Path(__file__).parent.parent / ".go-version"
GO_VERSION = go_version_file.read_text().strip()


class StaticSiteConfig:
    resource_name: str = "site"
    site_name: str = "personal-site"
    build_config: dict[str, str | bool] = {
        "build_caching": False,
        "build_command": "ls -la",
        "destination_dir": "/html",
        "root_dir": "/",
    }
    repo_name: str = ""
    domain_names: list[str] = [""]


def static_site(config: StaticSiteConfig):
    pages_projects = cloudflare.PagesProject(
        f"{config.resource_name}-pages-project",
        account_id=account_id,
        name=config.site_name,
        build_config=config.build_config,
        production_branch="main",
        source={
            "config": {
                "deployments_enabled": True,
                "pr_comments_enabled": True,
                "production_branch": "main",
                "production_deployments_enabled": True,
                "repo_name": config.repo_name,
                "owner": "brokensbone",
                "path_includes": ["*"],
            },
            "type": "github",
        },
        deployment_configs={
            "preview": {
                "env_vars": {
                    "test": {"type": "plain_text", "value": "some-value"},
                    "HUGO_VERSION": {"type": "plain_text", "value": HUGO_VERSION},
                    "GO_VERSION": {"type": "plain_text", "value": GO_VERSION},
                }
            },
            "production": {
                "env_vars": {
                    "test": {"type": "plain_text", "value": "prod-value"},
                    "HUGO_VERSION": {"type": "plain_text", "value": HUGO_VERSION},
                    "GO_VERSION": {"type": "plain_text", "value": GO_VERSION},
                }
            },
        },
    )

    for ix, domain_name in enumerate(config.domain_names):
        cloudflare.PagesDomain(
            f"{config.resource_name}-{ix}-pages-domain",
            account_id=account_id,
            project_name=pages_projects.name,
            name=domain_name,
        )
        cloudflare.DnsRecord(
            f"{config.resource_name}-{ix}-pages-dns",
            name=domain_name,
            proxied=True,
            ttl=1,
            type="CNAME",
            content=pages_projects.domains[0],
            zone_id=zone,
        )
    return pages_projects


def build():
    rnp_site = StaticSiteConfig()
    rnp_site.site_name = "rnp-blog"
    rnp_site.resource_name = "rnp"
    rnp_site.domain_names = [
        "rumandpopcorn.com",
        "www.rumandpopcorn.com",
    ]
    rnp_site.repo_name = "rumandpopcorn"
    rnp_site.build_config = {
        "build_caching": True,
        "build_command": "hugo",
        "destination_dir": "/public",
        "root_dir": "/rnp",
    }
    project = static_site(rnp_site)
    pulumi.export("latest_deployment", project.canonical_deployment)
