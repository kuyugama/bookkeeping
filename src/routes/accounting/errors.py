from src.error import define_error_category

define_error = define_error_category("accounting")

already_exist = define_error("already-exist", "Account already exist", 400)
reserved = define_error("reserved", "Reserved account name", 400)
not_found = define_error("not-found", "Account not found", 404)
