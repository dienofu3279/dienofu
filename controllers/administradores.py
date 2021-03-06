# -*- coding: utf-8 -*-
def inicio(): return dict(message="Hola desde administradores.py")

######################################### REGISTROS COMPLETOS #########################################

def listadoPlanes():
    datosPlanes = db().select(db.planes.ALL)
    i=0
    for x in datosPlanes:
         i=i+1
    return dict (datos=datosPlanes, cantidad=i)

def listadoCostos_instalaciones():
    datosCostos_instalaciones = db().select(db.costos_instalaciones.ALL)
    i=0
    for x in datosCostos_instalaciones:
         i=i+1
    return dict (datos=datosCostos_instalaciones, cantidad=i)

def listadoCostos_soportes():
    datosCostos_soportes = db().select(db.costos_soportes.ALL)
    i=0
    for x in datosCostos_soportes:
         i=i+1
    return dict (datos=datosCostos_soportes, cantidad=i)

def listadoNodos():
    datosNodos = db(db.nodos.localidad==db.localidades.id).select(db.nodos.ALL, db.localidades.ALL)
    i=0
    for x in datosNodos:
         i=i+1
    return dict (datos=datosNodos, cantidad=i)

def listadoPaneles():
    datosPaneles = db(db.paneles.nodo==db.nodos.id).select(db.paneles.ALL, db.nodos.ALL)
    i=0
    for x in datosPaneles:
         i=i+1
    return dict (datos=datosPaneles, cantidad=i)

######################################### SOLICITUDES DE INSTALACION #########################################

def alta_solicitud_instalacion():
    form = SQLFORM(db.solicitudes_instalacion)
    if form.accepts(request.vars, session):
        tipo = 1
        id_solicitud = db().select(db.solicitudes_instalacion.id).last().id
        redirect(URL(c="administradores", f="confirmacion_solicitud_instalacion", args=(tipo, id_solicitud)))
    elif form.errors:
        response.flash = 'El formulario tiene errores'
    else:
        response.flash = 'Complete el formulario'
    return dict(f=form)


def confirmacion_solicitud_instalacion():
    tipo = request.args[0]
    id_solicitud = request.args[1]
    return dict(tipo=tipo, id_solicitud=id_solicitud)

def editar_solicitud_instalacion():
    id_solicitud = request.args[0]
    tipo = 2
    solicitud =  db(db.solicitudes_instalacion.id == id_solicitud).select().first()
    form=SQLFORM(db.solicitudes_instalacion, solicitud)
    if form.accepts(request.vars, session):
        session.flash = 'Formulario correctamente cargado'
        redirect(URL(c="administradores", f="confirmacion_solicitud_instalacion", args=(tipo, id_solicitud)))
    elif form.errors:
        response.flash = 'Su formulario contiene errores, porfavor modifiquelo'
    else:
        response.flash = 'Por favor rellene el formulario'
    return dict(f=form)


def listadoSolicitudes_instalacion():
    solicitudesConTecnico = db((db.solicitudes_instalacion.localidad == db.localidades.id)&(db.solicitudes_instalacion.tipo_de_plan == db.planes.id)&(db.solicitudes_instalacion.costo_de_instalacion==db.costos_instalaciones.id)&(db.solicitudes_instalacion.tecnico == db.auth_user.id)).select(db.solicitudes_instalacion.ALL, db.localidades.ALL, db.planes.ALL, db.costos_instalaciones.ALL, db.auth_user.ALL)
    
    solicitudesSinTecnico = db((db.solicitudes_instalacion.localidad == db.localidades.id)&(db.solicitudes_instalacion.tipo_de_plan == db.planes.id)&(db.solicitudes_instalacion.costo_de_instalacion==db.costos_instalaciones.id)&(db.solicitudes_instalacion.tecnico == None)).select(db.solicitudes_instalacion.ALL, db.localidades.ALL, db.planes.ALL, db.costos_instalaciones.ALL)

    cantidadConTecnico=0
    for x in solicitudesConTecnico:
         cantidadConTecnico=cantidadConTecnico+1

    cantidadSinTecnico=0
    for x in solicitudesSinTecnico:
         cantidadSinTecnico=cantidadSinTecnico+1
    return dict (datos=solicitudesConTecnico, cantidad=cantidadConTecnico, datos2=solicitudesSinTecnico, cantidad2=cantidadSinTecnico)

def solicitudesDetalles():
    id_solicitud = request.args[0]
    solicitudesConTecnico = db((db.solicitudes_instalacion.id == id_solicitud)&(db.solicitudes_instalacion.localidad == db.localidades.id)&(db.solicitudes_instalacion.tipo_de_plan == db.planes.id)&(db.solicitudes_instalacion.costo_de_instalacion==db.costos_instalaciones.id)&(db.solicitudes_instalacion.tecnico == db.auth_user.id)).select(db.solicitudes_instalacion.ALL, db.localidades.ALL, db.planes.ALL, db.costos_instalaciones.ALL, db.auth_user.ALL)
    
    solicitudesSinTecnico = db((db.solicitudes_instalacion.id == id_solicitud)&(db.solicitudes_instalacion.localidad == db.localidades.id)&(db.solicitudes_instalacion.tipo_de_plan == db.planes.id)&(db.solicitudes_instalacion.costo_de_instalacion==db.costos_instalaciones.id)&(db.solicitudes_instalacion.tecnico == None)).select(db.solicitudes_instalacion.ALL, db.localidades.ALL, db.planes.ALL, db.costos_instalaciones.ALL)
    return dict (datos=solicitudesConTecnico, datos2=solicitudesSinTecnico)

######################################### SOLICITUDES SOPORTE #########################################

def solicitarSoporte():
    dni_recibido=request.vars.dni
    resultado = db((db.clientes.dni == dni_recibido)&(db.clientes.localidad==db.localidades.id)).select(db.clientes.ALL, db.localidades.ALL)
    if resultado:
        return dict(datos= resultado)
    else:
        return dict(datos=0)

def alta_solicitud_soporte():
    id_cliente = request.args[0]
    nombre = db(id_cliente == db.clientes.id).select(db.clientes.nombre)[0].nombre
    apellido = db(id_cliente == db.clientes.id).select(db.clientes.apellido)[0].apellido
    form = SQLFORM(db.solicitudes_soporte)
    form.vars.cliente = id_cliente
    if form.accepts(request.vars, session):
        tipo_conf = 2
        id_solicitud = db().select(db.solicitudes_soporte.id).last().id
        redirect(URL(c="administradores", f="confirmacion_solicitud_soporte", args=(tipo_conf, id_solicitud)))
    elif form.errors:
        response.flash = 'El formulario tiene errores'
    else:
        response.flash = 'Complete el formulario'
    return dict(f=form, nom=nombre, ape=apellido)

def confirmacion_solicitud_soporte():
    tipo_conf = request.args[0]
    id_solicitud = request.args[1]
    return dict(tipo_conf=tipo_conf, id_solicitud=id_solicitud)

def editar_solicitud_soporte():
    id_solicitud = request.args[0]
    solicitud =  db(db.solicitudes_soporte.id == id_solicitud).select().first()
    form=SQLFORM(db.solicitudes_soporte, solicitud)
    if form.accepts(request.vars, session):
        tipo_conf = 1
        redirect(URL(c="administradores", f="confirmacion_solicitud_soporte", args=(tipo_conf, id_solicitud)))
    elif form.errors:
		response.flash = 'Su formulario contiene errores, porfavor modifiquelo'
    else: 
		response.flash = 'Por favor rellene el formulario'
    return dict(f=form)

def listadoSolicitudes_soporte():
    solicitudesConTecnico = db((db.solicitudes_instalacion.tecnico == db.auth_user.id)&(db.solicitudes_soporte.cliente == db.clientes.id)).select(db.solicitudes_soporte.ALL, db.clientes.ALL, db.auth_user.ALL)
    
    solicitudesSinTecnico = db((db.solicitudes_soporte.tecnico == None)&(db.solicitudes_soporte.cliente == db.clientes.id)).select(db.solicitudes_soporte.ALL, db.clientes.ALL)
    
    cantidadConTecnico=0
    for x in solicitudesConTecnico:
         cantidadConTecnico=cantidadConTecnico+1

    cantidadSinTecnico=0
    for x in solicitudesSinTecnico:
         cantidadSinTecnico=cantidadSinTecnico+1
            
    return dict (datos=solicitudesConTecnico, cantidad=cantidadConTecnico, datos2=solicitudesSinTecnico, cantidad2=cantidadSinTecnico)

######################################### CONSULTAS #########################################

def clientes_dni():
    dni_recibido=request.vars.dni
    resultado = db((db.clientes.dni == dni_recibido)&(db.clientes.localidad==db.localidades.id)).select(db.clientes.ALL, db.localidades.ALL)
    if resultado:
        return dict(datos= resultado)
    else:
        return dict(datos=0)

def clientes_nombre_apellido():
    nom=request.vars.nom_ape
    if nom != None:
        resultado = db(
            ((db.clientes.nombre.lower()==nom.lower())&(db.clientes.localidad == db.localidades.id)) |
            ((db.clientes.apellido.lower()==nom.lower())&(db.clientes.localidad == db.localidades.id)) |
            ((db.clientes.nombre.lower() + ' ' + db.clientes.apellido.lower() == nom.lower())&(db.clientes.localidad == db.localidades.id)) |
            ((db.clientes.nombre.lower().contains(nom.lower()))&(db.clientes.localidad == db.localidades.id)) |
            ((db.clientes.apellido.lower().contains(nom.lower()))&(db.clientes.localidad == db.localidades.id))).select(db.clientes.ALL, db.localidades.ALL)
        if resultado:
            return dict(datos= resultado)
        else:
            return dict(datos=0)
    else:
        return dict(datos="None")

def clientes_ip():
    i=0
    cliente =db().select(db.clientes.ALL)
    for x in cliente:
        i= i+1
    return dict(datos=cliente, cantidad=i)

def listadoClientes():
    datosClientes = db((db.clientes.localidad==db.localidades.id)&(db.clientes.tipo_de_plan==db.planes.id)&(db.clientes.numero_de_instalacion == db.instalaciones.id)&(db.instalaciones.panel == db.paneles.id)).select(db.clientes.ALL, db.localidades.localidad, db.paneles.ALL, db.planes.ALL)
    i=0
    for x in datosClientes:
         i=i+1
    return dict (datos=datosClientes, cantidad=i)

def clientesDetalles():
    id_cliente = request.args[0]
    resultado = db((db.clientes.id == id_cliente)&(db.clientes.localidad==db.localidades.id)&(db.clientes.tipo_de_plan==db.planes.id)&(db.clientes.numero_de_instalacion == db.instalaciones.id)&(db.instalaciones.panel == db.paneles.id)).select(db.clientes.ALL, db.localidades.localidad, db.paneles.ALL, db.planes.ALL, db.instalaciones.ALL)
    return dict(datos=resultado)

######################################### HERRAMIENTAS #########################################

def coords_by_address(direccion):
    import re, urllib
    try:
        address=urllib.quote(direccion)
        #url='http://maps.google.com/maps/geo?q=%s&output=xml'%address
        key = KEY_API_GOOGLE_MAP
        url='https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s' % (address, key)

        response = urllib.urlopen(url).read()
        import json
        ret = json.loads(response)
        #item=re.compile('\<coordinates\>(?P<la>[^,]),(?P<lo>[^,]).*?\</coordinates\>').search(t)
        #la,lo=float(item.group('la')),float(item.group('lo'))
        la = ret["results"][0]["geometry"]["location"]["lat"]
        lo = ret["results"][0]["geometry"]["location"]["lng"]
        return la,lo,url
    except Exception, e: 
        #raise RuntimeError(str(e))
        pass
        raise
    #raise RuntimeError(str("%s = %s" % (address, t)))
    return 0.0,0.0,url

def actualizar_coords():
    if request.args:
        id_solicitud = request.args[0]
        ret = ""
        for reg in db((db.solicitudes_instalacion.localidad == db.localidades.id)&(id_solicitud == db.solicitudes_instalacion.id)).select(db.solicitudes_instalacion.id, db.solicitudes_instalacion.direccion, db.solicitudes_instalacion.numero_de_calle, db.localidades.localidad, db.localidades.codigo_postal):
            dom = "%s %s, %s, %s, %s" % (reg.solicitudes_instalacion.direccion, reg.solicitudes_instalacion.numero_de_calle, reg.localidades.localidad,"buenos aires","argentina")
            lat, lon , url = coords_by_address(dom)
            db(db.solicitudes_instalacion.id==reg.solicitudes_instalacion.id).update(latitud=lat, longitud=lon)
            ret += "solicitante: %s coords= %s,%s url: %s\n\r" % (reg.solicitudes_instalacion.id, lat, lon, url)
            mensaje = "¡Se ha actualizado la ubicación!"
        return dict (mensaje = mensaje)
    else:
        ret = ""
        for reg in db(db.solicitudes_instalacion.localidad == db.localidades.id).select(db.solicitudes_instalacion.id, db.solicitudes_instalacion.direccion, db.solicitudes_instalacion.numero_de_calle, db.localidades.localidad, db.localidades.codigo_postal):
            dom = "%s %s, %s, %s, %s" % (reg.solicitudes_instalacion.direccion, reg.solicitudes_instalacion.numero_de_calle, reg.localidades.localidad,"buenos aires","argentina")
            lat, lon , url = coords_by_address(dom)
            db(db.solicitudes_instalacion.id==reg.solicitudes_instalacion.id).update(latitud=lat, longitud=lon)
            ret += "solicitante: %s coords= %s,%s url: %s\n\r" % (reg.solicitudes_instalacion.id, lat, lon, url)
            mensaje = "¡Se han actualizado todas las ubicaciones!"
        return dict (mensaje = mensaje)

def geolocalizacionClientes():
    rows=db((db.clientes.id>0)&(db.clientes.localidad==db.localidades.id)).select(
            db.clientes.nombre,
            db.clientes.apellido,
            db.clientes.direccion,
            db.clientes.numero_de_calle,
            db.localidades.localidad,
            db.clientes.latitud,
            db.clientes.longitud)
    x0,y0= COORDS_INICIO_MAPA
    d = dict(x0=x0,y0=y0,rows=rows)
    return response.render(d)

def geolocalizacionNodos():
    d = 4
    return dict(datos=d)

######################################### OTRAS #########################################

import datetime
from ConfigParser import SafeConfigParser
from pyafipws.pyfepdf import FEPDF
from pyafipws.wsaa import WSAA
from pyafipws.wsfev1 import WSFEv1

def obtener_cae():
    # web service de factura electronica:
    wsfev1 = WSFEv1()
    wsfev1.LanzarExcepciones = True

    # obteniendo el TA para pruebas
    ta = WSAA().Autenticar("wsfe", "/home/rodrigo/pyafipws/staff.crt",
                                   "/home/rodrigo/pyafipws/staff.key", debug=True)
    wsfev1.SetTicketAcceso(ta)
    wsfev1.Cuit = "20267565393"

    ok = wsfev1.Conectar()

    tipo_cbte = 6
    punto_vta = 4001
    cbte_nro = long(wsfev1.CompUltimoAutorizado(tipo_cbte, punto_vta) or 0)
    fecha = datetime.datetime.now().strftime("%Y%m%d")
    concepto = 1
    tipo_doc = 80 # 80: CUIT, 96: DNI
    nro_doc = "30500010912" # del cliente
    cbt_desde = cbte_nro + 1; cbt_hasta = cbte_nro + 1
    imp_total = "222.00"
    imp_tot_conc = "0.00"
    imp_neto = "200.00"
    imp_iva = "21.00"
    imp_trib = "1.00"
    imp_op_ex = "0.00"
    fecha_cbte = fecha
    # Fechas del per�odo del servicio facturado y vencimiento de pago:
    if concepto > 1:
        fecha_venc_pago = fecha
        fecha_serv_desde = fecha
        fecha_serv_hasta = fecha
    else:
        fecha_venc_pago = fecha_serv_desde = fecha_serv_hasta = None
    moneda_id = 'PES'
    moneda_ctz = '1.000'

    wsfev1.CrearFactura(concepto, tipo_doc, nro_doc, 
                tipo_cbte, punto_vta, cbt_desde, cbt_hasta , 
                imp_total, imp_tot_conc, imp_neto,
                imp_iva, imp_trib, imp_op_ex, fecha_cbte, fecha_venc_pago, 
                fecha_serv_desde, fecha_serv_hasta, #--
                moneda_id, moneda_ctz)

    # otros tributos:
    tributo_id = 99
    desc = 'Impuesto Municipal Matanza'
    base_imp = None
    alic = None
    importe = 1
    wsfev1.AgregarTributo(tributo_id, desc, base_imp, alic, importe)

    # subtotales por alicuota de IVA:
    iva_id = 3 # 0%
    base_imp = 100    # neto al 0%
    importe = 0
    wsfev1.AgregarIva(iva_id, base_imp, importe)

    # subtotales por alicuota de IVA:
    iva_id = 5 # 21%
    base_imp = 100   # neto al 21%
    importe = 21     # iva liquidado al 21%
    wsfev1.AgregarIva(iva_id, base_imp, importe)

    wsfev1.CAESolicitar()

    print "Nro. Cbte. desde-hasta", wsfev1.CbtDesde, wsfev1.CbtHasta
    print "Resultado", wsfev1.Resultado
    print "Reproceso", wsfev1.Reproceso
    print "CAE", wsfev1.CAE
    print "Vencimiento", wsfev1.Vencimiento
    print "Observaciones", wsfev1.Obs

    session.cae = wsfev1.CAE
    response.view = "generic.html"
    return {"Nro. Cbte. desde-hasta": wsfev1.CbtDesde,
            "Resultado": wsfev1.Resultado,
            "Reproceso": wsfev1.Reproceso,
            "CAE": wsfev1.CAE,
            "Vencimiento": wsfev1.Vencimiento,
            "Observaciones": wsfev1.Obs,
          }

def generar_pdf(): 
    CONFIG_FILE = "/home/rodrigo/pyafipws/rece.ini"

    config = SafeConfigParser()
    config.read(CONFIG_FILE)
    conf_fact = dict(config.items('FACTURA'))
    conf_pdf = dict(config.items('PDF'))

    fepdf = FEPDF()

    # cargo el formato CSV por defecto (factura.csv)
    fepdf.CargarFormato(conf_fact.get("formato", "factura.csv"))

    # establezco formatos (cantidad de decimales) según configuración:
    fepdf.FmtCantidad = conf_fact.get("fmt_cantidad", "0.2")
    fepdf.FmtPrecio = conf_fact.get("fmt_precio", "0.2")


    # creo una factura de ejemplo
    HOMO = True

    # datos generales del encabezado:
    tipo_cbte = 1
    punto_vta = 4000
    fecha = datetime.datetime.now().strftime("%Y%m%d")
    concepto = 3
    tipo_doc = 80; nro_doc = "30000000007"
    cbte_nro = 12345678
    imp_total = "127.00"
    imp_tot_conc = "3.00"
    imp_neto = "100.00"
    imp_iva = "21.00"
    imp_trib = "1.00"
    imp_op_ex = "2.00"
    imp_subtotal = "105.00"
    fecha_cbte = fecha
    fecha_venc_pago = fecha
    # Fechas del período del servicio facturado (solo si concepto> 1)
    fecha_serv_desde = fecha
    fecha_serv_hasta = fecha
    # campos p/exportación (ej): DOL para USD, indicando cotización:
    moneda_id = 'PES'
    moneda_ctz = 1
    incoterms = 'FOB'                   # solo exportación
    idioma_cbte = 1                     # 1: es, 2: en, 3: pt

    # datos adicionales del encabezado:
    nombre_cliente = 'Juan Perez'
    domicilio_cliente = 'Rua 76 km 34.5 Alagoas'
    pais_dst_cmp = 212                  # 200: Argentina, ver tabla
    id_impositivo = 'PJ54482221-l'      # cat. iva (mercado interno)
    forma_pago = '30 dias'

    obs_generales = "Observaciones Generales<br/>linea2<br/>linea3"
    obs_comerciales = "Observaciones Comerciales<br/>texto libre"

    # datos devueltos por el webservice (WSFEv1, WSMTXCA, etc.):
    motivo_obs = "Factura individual, DocTipo: 80, DocNro 30000000007 no se encuentra registrado en los padrones de AFIP."
    cae = session.cae
    fch_venc_cae = "20110320"

    fepdf.CrearFactura(concepto, tipo_doc, nro_doc, tipo_cbte, punto_vta,
        cbte_nro, imp_total, imp_tot_conc, imp_neto,
        imp_iva, imp_trib, imp_op_ex, fecha_cbte, fecha_venc_pago, 
        fecha_serv_desde, fecha_serv_hasta, 
        moneda_id, moneda_ctz, cae, fch_venc_cae, id_impositivo,
        nombre_cliente, domicilio_cliente, pais_dst_cmp, 
        obs_comerciales, obs_generales, forma_pago, incoterms, 
        idioma_cbte, motivo_obs)

    # completo campos extra del encabezado:
    ok = fepdf.EstablecerParametro("localidad_cliente", "Hurlingham")
    ok = fepdf.EstablecerParametro("provincia_cliente", "Buenos Aires")

    # imprimir leyenda "Comprobante Autorizado" (constatar con WSCDC!)
    ok = fepdf.EstablecerParametro("resultado", "A")

    # tributos adicionales:
    tributo_id = 99
    desc = 'Impuesto Municipal Matanza'
    base_imp = "100.00"
    alic = "1.00"
    importe = "1.00"
    fepdf.AgregarTributo(tributo_id, desc, base_imp, alic, importe)

    tributo_id = 4
    desc = 'Impuestos Internos'
    base_imp = None
    alic = None
    importe = "0.00"
    fepdf.AgregarTributo(tributo_id, desc, base_imp, alic, importe)

    # subtotales por alícuota de IVA:
    iva_id = 5 # 21%
    base_imp = 100
    importe = 21
    fepdf.AgregarIva(iva_id, base_imp, importe)

    # detalle de artículos:
    u_mtx = 123456
    cod_mtx = 1234567890123
    codigo = "P0001"
    ds = "Descripcion del producto P0001\n"
    qty = 1.00
    umed = 7
    if tipo_cbte in (1, 2, 3, 4, 5, 34, 39, 51, 52, 53, 54, 60, 64):
        # discriminar IVA si es clase A / M
        precio = 110.00
        imp_iva = 23.10
    else:
        # no discriminar IVA si es clase B (importe final iva incluido)
        precio = 133.10
        imp_iva = None
    bonif = 0.00
    iva_id = 5
    importe = 133.10
    despacho = u'Nº 123456'
    dato_a = "Dato A"
    fepdf.AgregarDetalleItem(u_mtx, cod_mtx, codigo, ds, qty, umed, 
            precio, bonif, iva_id, imp_iva, importe, despacho, dato_a)

    # descuento general (a tasa 21%):
    u_mtx = cod_mtx = codigo = None
    ds = u"Bonificación/Descuento 10%"
    qty = precio = bonif = None
    umed = 99
    iva_id = 5
    if tipo_cbte in (1, 2, 3, 4, 5, 34, 39, 51, 52, 53, 54, 60, 64):
        # discriminar IVA si es clase A / M
        imp_iva = -2.21
    else:
        imp_iva = None
    importe = -12.10
    fepdf.AgregarDetalleItem(u_mtx, cod_mtx, codigo, ds, qty, umed, 
            precio, bonif, iva_id, imp_iva, importe, "")

    # descripción (sin importes ni cantidad):
    u_mtx = cod_mtx = codigo = None
    qty = precio = bonif = iva_id = imp_iva = importe = None
    umed = 0
    ds = u"Descripción Ejemplo"
    fepdf.AgregarDetalleItem(u_mtx, cod_mtx, codigo, ds, qty, umed, 
            precio, bonif, iva_id, imp_iva, importe, "")

    # completo campos personalizados de la plantilla:
    fepdf.AgregarDato("custom-nro-cli", "Cod.123")
    fepdf.AgregarDato("custom-pedido", "1234")
    fepdf.AgregarDato("custom-remito", "12345")
    fepdf.AgregarDato("custom-transporte", "Camiones Ej.")
    print "Prueba!"
    
    # datos fijos:
    for k, v in conf_pdf.items():
        fepdf.AgregarDato(k, v)
        if k.upper() == 'CUIT':
            fepdf.CUIT = v  # CUIT del emisor para código de barras

    fepdf.CrearPlantilla(papel=conf_fact.get("papel", "legal"), 
                         orientacion=conf_fact.get("orientacion", "portrait"))
    fepdf.ProcesarPlantilla(num_copias=int(conf_fact.get("copias", 1)),
                            lineas_max=int(conf_fact.get("lineas_max", 24)),
                            qty_pos=conf_fact.get("cant_pos") or 'izq')

    salida = "/tmp/factura.pdf"
    fepdf.GenerarPDF(archivo=salida)
    ##fepdf.MostrarPDF(archivo=salida,imprimir=False)

    response.headers['Content-Type'] = "application/pdf"
    return open(salida, "rb")
