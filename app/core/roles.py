class Role:
    ADMIN = "admin"
    OWNER = "owner"
    MEMBER = "member"


ROLE_LEVELS = {
    Role.MEMBER: 1,
    Role.ADMIN: 2,
    Role.OWNER: 3
}
