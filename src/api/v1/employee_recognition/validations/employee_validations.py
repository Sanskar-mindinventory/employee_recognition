
class Validation:
    @staticmethod
    def name_validation(name):
        if len(name) <= 1 or len(name) > 30:
            raise ValueError("Name length must be between 2 to 30 characters ")
        return name