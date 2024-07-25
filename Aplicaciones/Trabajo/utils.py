#restricciones por roles de ususarios
def is_admin(usuario):
    return usuario.is_authenticated and (usuario.rol_id == 1 or usuario.rol_id == 2)

def is_prod(usuario):
    return usuario.is_authenticated and usuario.rol_id == 3
def is_recep(usuario):
    return usuario.is_authenticated and usuario.rol_id == 4
def is_cal(usuario):
    return usuario.is_authenticated and usuario.rol_id == 5

def is_admin_recep(usuario):
    return usuario.is_authenticated and (usuario.rol_id == 1 or usuario.rol_id == 2 or usuario.rol_id == 4)

def is_admin_prod(usuario):
        return usuario.is_authenticated and (usuario.rol_id == 1 or usuario.rol_id == 2 or usuario.rol_id == 3)

def is_admin_cal(usuario):
        return usuario.is_authenticated and (usuario.rol_id == 1 or usuario.rol_id == 2 or usuario.rol_id == 5)
