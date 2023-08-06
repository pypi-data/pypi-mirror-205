from enum import EnumMeta


class _ValidatorEnumMeta(EnumMeta):
    @staticmethod
    def _validate_types(classdict, desired_type):
        if isinstance(classdict._member_names, list):  # pragma: no cover
            member_names = [member_name for member_name in classdict._member_names]
        else:  # pragma: no cover
            member_names = [
                member_name for member_name in classdict._member_names.keys()
            ]
        member_dict = {
            member_name: classdict[member_name] for member_name in member_names
        }

        for member_name, member_value in member_dict.items():
            if not isinstance(member_value, desired_type):
                raise TypeError(f"{member_name} is not a valid State")
