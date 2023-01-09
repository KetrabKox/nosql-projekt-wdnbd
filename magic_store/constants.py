class MESSAGES:
    OK_CODE = 100
    INCORRECT_NAMESPACE_CODE = 202
    INCORRECT_KEY_CODE = 203
    INCORRECT_GUARD_CODE = 205
    INCORRECT_TYPE_CODE = 207

    OK = {"code": OK_CODE, "success":True, "description": "OK"}
    INCORRECT_NAMESPACE = {"code": INCORRECT_NAMESPACE_CODE,"success":False, "description": "Incorrect (nonexisting) namespace"}
    INCORRECT_KEY = {"code": INCORRECT_KEY_CODE,"success":False, "description": "Incorrect key"}
    INCORRECT_GUARD = {"code": INCORRECT_GUARD_CODE,"success":False,"description": "Incorrect guard"}
    INCORRECT_TYPE = {"code": INCORRECT_TYPE_CODE,"success":False, "description": "Incorrect type"}

    @classmethod
    def ok(cls, value, guard):
        result = cls.OK.copy()
        result["value"] = value
        result["guard"] = guard
        return result