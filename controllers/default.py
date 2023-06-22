# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------
# ---- example index page ----
from datetime import date, timedelta,datetime
from gluon.tools import Mail
def index():
    return dict(productos=db(db.modelos).select(),colecciones=db(db.colecciones.banner).select())
 
# ---- Action for login/register/etc (required for auth) -----
def user():
    return dict(form=auth())

@auth.requires_login()
def profile():
    return dict(profile=auth.user)

@auth.requires_login()
def cart():
    return dict(cart = db(db.carrito.usuario == auth.user.id).select(join=db.carrito.on(db.modelos.id == db.carrito.producto)), total=0)

@auth.requires_login()
def eliminar():
    id = request.args(0) or redirect(URL('index'))
    db(db.carrito.id == id).delete()
    return redirect(URL('default','cart'))

@auth.requires_login()
def limpiar():
    db(db.carrito.usuario == auth.user.id).delete()
    return redirect(URL('default','cart'))

def product_details():
    modelo = db.modelos(request.args(0)) or redirect(URL('index'))
    rows = db(db.modelos.id == modelo.id).select(join=db.modelos.on(db.colecciones.id == db.modelos.coleccion))
    return dict(product = rows.first())

@auth.requires_login()
def agregar():
    id = request.args(0) or redirect(URL('index'))    
    db.carrito.insert(usuario=auth.user.id,producto=id)
    response.flash = T('¡Producto agregado!')
    return redirect(URL('index'))    
# ---- action to server uploaded static content (required) ---

@auth.requires_login()
def addresses():
    return dict(direcciones = db(db.direcciones.usuario==auth.user.id).select())

@auth.requires_login()
def new_address():
    form = SQLFORM(db.direcciones)
    form.vars.usuario = auth.user.id
    if form.process(session=None, formname='new_address').accepted:
        response.flash = T('nueva direccion agregada')
    elif form.errors:
        for campo in form.errors:
            response.flash = T(form.errors[campo])   
    return dict()    

@auth.requires_login()
def checkout():
    return dict(direcciones = db(db.direcciones.usuario == auth.user.id).select(),cart = db(db.carrito.usuario == auth.user.id).select(join=db.carrito.on(db.modelos.id == db.carrito.producto)), total=0)    

@auth.requires_login()
def crear_orden():
    idpedido = db.pedidos.insert(cliente=auth.user.id,direccion=request.vars.direccion,estado=1,entrega=date.today()+timedelta(weeks=1),fecha=datetime.now(),total=request.vars.total)
    cart = db(db.carrito.usuario == auth.user.id).select(join=db.carrito.on(db.modelos.id == db.carrito.producto))
    for item in cart:
        db.desglose_pedidos.insert(pedido=idpedido,diseño=item.carrito.producto,precio=item.modelos.precio,cantidad=1,estado=1)
    db(db.carrito.usuario == auth.user.id).delete()    
    return dict()

@auth.requires_login()
def orders():
    return dict(ordenes = db(db.pedidos.cliente == auth.user.id).select(join=db.pedidos.on(db.estados.id == db.pedidos.estado)))

@auth.requires_login()
def order_details():
    idpedido = request.args(0) or redirect(URL('index'))
    return dict(pedido = db(db.desglose_pedidos.pedido==idpedido).select(join=db.desglose_pedidos.on(db.modelos.id == db.desglose_pedidos.diseño)))

@auth.requires_login()
@auth.requires_membership('empleado')
def orders_employee():
    grid = SQLFORM.smartgrid(db.pedidos)
    return locals()

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

