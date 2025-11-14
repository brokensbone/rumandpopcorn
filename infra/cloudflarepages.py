import pulumi
import pulumi_cloudflare as cloudflare

config = pulumi.Config("rnp")
zone = config.require_secret("zone_id")
account_id = config.require_secret("account_id")


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
        deployment_configs={
            "production": {
                "environment_variables": {
                    "HUGO_VERSION": "0.147.6",
                },
            },
            "preview": {
                "environment_variables": {
                    "HUGO_VERSION": "0.147.6",
                },
            },
        },
        source={
            "config": {
                "deployments_enabled": True,
                "pr_comments_enabled": True,
                "production_branch": "main",
                "production_deployments_enabled": True,
                "repo_name": config.repo_name,
                "owner": "brokensbone",
            },
            "type": "github",
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
    static_site(rnp_site)
