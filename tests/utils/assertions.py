from .adapters import convert_datetime_to_date


def compare_entities_without_id_and_created_at(result, expected):
    for idx, item in enumerate(result):
        assert all(
            item.model_dump()[k] == expected[idx].model_dump()[k]
            for k in list(
                set(item.model_dump().keys())
                - set(
                    [
                        "id",
                        "debt_since",
                        "debtors",
                        "created_at",
                        "partner_national_id",
                        "group",
                    ]
                )
            )
        )
        result_debt_since = convert_datetime_to_date(item.model_dump()["debt_since"])
        expected_debt_since = convert_datetime_to_date(
            expected[idx].model_dump()["debt_since"]
        )
        assert result_debt_since == expected_debt_since
