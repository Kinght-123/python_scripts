from functools import wraps


def check_permission(permission, ignore=False, raise_exception=False):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if permission not in self.user.permissions:
                if raise_exception:
                    return
                elif not ignore:
                    return
            return func(self, *args, **kwargs)

        return wrapper

    return decorator


class User:
    def __init__(self, permissions):
        self.permissions = permissions


class Action:
    def __init__(self, user):
        self.user = user

    @check_permission("edit", ignore=True)
    def edit_document(self, document_id):
        print(f"Editing document {document_id}")

    @check_permission("delete", raise_exception=True)
    def delete_document(self, document_id):
        print(f"Deleting document {document_id}")


user = User(["edit"])
action = Action(user)

action.edit_document(1)  # 正常执行
action.delete_document(1)  # 抛出 PermissionError