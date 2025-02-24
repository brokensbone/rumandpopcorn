import pulumiverse_statuscake as statuscake


def build_statuscake_check():
    contact_group_resource = statuscake.ContactGroup("contactGroupResource",
        email_addresses=["administrator@rumandpopcorn.com"],
    )

    return statuscake.UptimeCheck("uptimeCheckResource",
        check_interval=300,
        monitored_resource={
            "address": "https://rumandpopcorn.com",
        },
        contact_groups=[contact_group_resource.id],
        http_check={
            "status_codes": [
                "100", "101", "102", "103", "201", "202", "203", "204", "205", "206", "207", "208", "226",
                "300", "301", "302", "303", "304", "305", "306", "307", "308",
                "400", "401", "402", "403", "404", "405", "406", "407", "408", "409", "410", "411", "412", "413", "414", "415", "416", "417", "418", "421", "422", "423", "424", "425", "426", "428", "429", "431", "451",
                "500", "501", "502", "503", "504", "505", "506", "507", "508", "510", "511"
            ],
        },
        confirmation=0,
        name="Rum And Popcorn Check",
    )