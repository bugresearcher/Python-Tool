#!/usr/bin/python
#-*- coding:utf-8 -*-

##############################################################################
# İllegalsecurity - CodeNinja
# TcKimlikSorgula
# nvi.gov.tr sitesinden tckimlik sorgular ve tckimlik bilgilerini getirir
# 11.10.2016
##############################################################################

#Soap için kurulum paketi
#sudo aptitude install python-soappy
import os, random, time, re, sys
import base64, binascii
import hashlib
import pycurl
import StringIO
from datetime import datetime

os.environ['TZ']    = 'UTC'
WSDL_URL            = '[url]https://kps.nvi.gov.tr:443/Mernis.KPS.Web.si/kps.asmx[/url]'
WSDL_FUNC           = 'TCKimlikNodanKisiBilgisiSorgula'
USERNAME            = 'XXXXXXXXXX'
PASSWORD            = 'XXXXXXXXXX'
TCKIMLIKNO          = 'XXXXXXXXXX'

#-----------------------------------------------------------------------------
# Rasgele 10 haneli sayı oluştur
def passwordOlustur():
    vMakePass   = ""
    vSalt       = random.sample(xrange(10),8)
    for i in vSalt:
        vMakePass += str(i)
    return vMakePass 

#-----------------------------------------------------------------------------
# Sorguya çıkmak için gerekli değerleri oluştur.
def getVariable():
    rndnum      = passwordOlustur()
    nonce       = base64.encodestring(rndnum)
    #nonce       = binascii.b2a_base64(rndnum)
    timestamp   = int(time.time())
    #oluşturma zamanı
    created     = timestamp - 3000
    created     = datetime.fromtimestamp(created)
    created     = created.strftime('%Y-%m-%dT%H:%M:%SZ')
    #session sonlanma zamanı
    expires     = timestamp
    expires     = datetime.fromtimestamp(expires)
    expires     = expires.strftime('%Y-%m-%dT%H:%M:%SZ')
    parola      = hashlib.sha1(rndnum+created+PASSWORD)
    parola      = parola.digest()
    parola      = base64.encodestring(parola)
    #parola      = binascii.b2a_base64(parola)

    print  """
            ------------------------------------------------------------------
            Oluşturulan Değerler
            ------------------------------------------------------------------
            rndnum      :%s
            nonce       :%s
            timestamp   :%d
            created     :%s
            expires     :%s
            parola      :%s
            wsdlfunc    :%s
           """ % (rndnum,nonce,timestamp,created,expires,parola,WSDL_FUNC)
    return (rndnum,nonce,(timestamp),created,expires,parola)

#-----------------------------------------------------------------------------
# Sorgu İçin Header Oluştur
def getHeader(sNonce,sCreated,sExpires,sUserName, sParola):
    securityParams = {
        'PasswordDigest': sParola,
        'Username': sUserName,
        'Nonce': sNonce,
        'Created': sCreated,
        'Expires': sExpires
    }
    header = """
    <SOAP-ENV:Header>
        <wsse:Security SOAP-ENV:mustUnderstand="1">
            <wsu:Timestamp wsu:Id="Timestamp-daf6faf7-798a-4084-a596-44c421ca1c27">
                <wsu:Created>%(Created)s</wsu:Created>
                <wsu:Expires>%(Expires)s</wsu:Expires>
            </wsu:Timestamp>
            <wsse:UsernameToken wsu:Id="SecurityToken-500224e8-41be-4350-a5a6-8de59e7dde8f">
                <wsse:Username>%(Username)s</wsse:Username>
                <wsse:Password Type="[url]http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordDigest[/url]">%(PasswordDigest)s</wsse:Password>
                <wsse:Nonce>%(Nonce)s</wsse:Nonce>
                <wsu:Created>%(Created)s</wsu:Created>
            </wsse:UsernameToken>
        </wsse:Security>
    </SOAP-ENV:Header>""" % securityParams
    return header

#-----------------------------------------------------------------------------
# Sorgu için Msg Oluştur
def getMsg(sTcKimlikNo,sNonce,sCreated,sExpires,sUserName,sParola):
    msg = """<?xml version="1.0" encoding="utf-8"?>
    <SOAP-ENV:Envelope xmlns:SOAP-ENV="[url]http://schemas.xmlsoap.org/soap/envelope/[/url]" xmlns:xsd="[url]http://www.w3.org/2001/XMLSchema[/url]" xmlns:xsi="[url]http://www.w3.org/2001/XMLSchema-instance[/url]" xmlns:wsa="[url]http://schemas.xmlsoap.org/ws/2004/03/addressing[/url]" xmlns:wsse="[url]http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd[/url]" xmlns:wsu="[url]http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd[/url]" xmlns:SOAP-ENC="[url]http://schemas.xmlsoap.org/soap/encoding/[/url]">
    %s
    <SOAP-ENV:Body>
        <TCKimlikNodanKisiBilgisiSorgula xmlns="[url]http://kps.nvi.gov.tr/WS[/url]">
            <list>
                <TCKimlikNoG>
                    <TCKimlikNo>%s</TCKimlikNo>
                </TCKimlikNoG>
            </list>
        </TCKimlikNodanKisiBilgisiSorgula>
    </SOAP-ENV:Body>
</SOAP-ENV:Envelope>
    """ % (getHeader(sNonce,sCreated,sExpires,sUserName, sParola),sTcKimlikNo)
    return msg

#-----------------------------------------------------------------------------
# Hata Kodu kısmını getirir
def getHatakodu(sVal):
    sablon = re.compile('<HataKod>(.*?)</HataKod>', re.DOTALL)
    stil   = sablon.search(sVal)
    return stil.group(1)

#-----------------------------------------------------------------------------
# Sorgu pozisyon kısmını getir
def getSorgupozisyon(sVal):
    try:
        sablon = re.compile('<SorguPozisyon>(.*?)</SorguPozisyon>', re.DOTALL)
        stil   = sablon.search(sVal)
        return stil.group(1)
    except: return '-1'
#-----------------------------------------------------------------------------
# Tckimlikno kısmını getir
def getTckimlikno(sVal):
    try:
        sablon = re.compile('<TCKimlikNo>(.*?)</TCKimlikNo>', re.DOTALL)
        stil   = sablon.search(sVal)
        return stil.group(1)
    except: return '-1'

#-----------------------------------------------------------------------------
# Ad kısmını getir
def getAd(sVal):
    try:
        sablon = re.compile('<Ad>(.*?)</Ad>', re.DOTALL)
        stil   = sablon.search(sVal)
        return stil.group(1)
    except: return '-1'

#-----------------------------------------------------------------------------
# Soyad kısmını getir
def getSoyad(sVal):
    try:
        sablon = re.compile('<Soyad>(.*?)</Soyad>', re.DOTALL)
        stil   = sablon.search(sVal)
        return stil.group(1)
    except: return '-1'

#-----------------------------------------------------------------------------
# Cinsiyet kısmını getir
def getCinsiyet(sVal):
    try:
        sablon = re.compile('<Cinsiyet>(.*?)</Cinsiyet>', re.DOTALL)
        stil   = sablon.search(sVal)
        return stil.group(1)
    except: return '-1'

#-----------------------------------------------------------------------------
# Babaad kısmını getir
def getBabaad(sVal):
    try:
        sablon = re.compile('<BabaAd>(.*?)</BabaAd>', re.DOTALL)
        stil   = sablon.search(sVal)
        return stil.group(1)
    except: return '-1'

#-----------------------------------------------------------------------------
# Baba Soyad kısmını getir
def getBabasoyad(sVal):
    try:
        sablon = re.compile('<BabaSoyad>(.*?)</BabaSoyad>', re.DOTALL)
        stil   = sablon.search(sVal)
        return stil.group(1)
    except: return '-1'

#-----------------------------------------------------------------------------
# Ana adı kısmını getir
def getAnaad(sVal):
    try:
        sablon = re.compile('<AnaAd>(.*?)</AnaAd>', re.DOTALL)
        stil   = sablon.search(sVal)
        return stil.group(1)
    except: return '-1'

#-----------------------------------------------------------------------------
# Ana Soyad kısmını getir
def getAnasoyad(sVal):
    try:
        sablon = re.compile('<AnaSoyad>(.*?)</AnaSoyad>', re.DOTALL)
        stil   = sablon.search(sVal)
        return stil.group(1)
    except: return '-1'

#-----------------------------------------------------------------------------
# Doğum tarihi kısmını getir
def getDogumtarihi(sVal):
    try:
        sablon = re.compile('<DogumTarih><Yil>(.*?)</Yil><Ay>(.*?)</Ay><Gun>(.*?)</Gun></DogumTarih>', re.DOTALL)
        stil   = sablon.search(sVal)
        return stil.group(1) + "-" + stil.group(2)  + "-" + stil.group(3)
    except: return '-1'

#-----------------------------------------------------------------------------
# Doğum yeri kısmını getir
def getDogumyeri(sVal):
    try:
        sablon = re.compile('<DogumYer>(.*?)</DogumYer>', re.DOTALL)
        stil   = sablon.search(sVal)
        return stil.group(1)
    except: return '-1'

#-----------------------------------------------------------------------------
# Kızlık Soyadı kısmını getir
def getKizliksoyadi(sVal):
    try:
        sablon = re.compile('<KizlikSoyad>(.*?)</KizlikSoyad>', re.DOTALL)
        stil   = sablon.search(sVal)
        return stil.group(1)
    except: return '-1'

#-----------------------------------------------------------------------------
# Özür Oran kısmını getir
def getOzuroran(sVal):
    try:
        sablon = re.compile('<OzurOran>(.*?)</OzurOran>', re.DOTALL)
        stil   = sablon.search(sVal)
        return stil.group(1)
    except: return '-1'

#-----------------------------------------------------------------------------
# Durum kısmını getir
def getDurum(sVal):
    try:
        sablon = re.compile('<Durum>(.*?)</Durum>', re.DOTALL)
        stil   = sablon.search(sVal)
        return stil.group(1)
    except: return '-1'

#-----------------------------------------------------------------------------
# Medeni Hal kısmını getir
def getMedenihal(sVal):
    try:
        sablon = re.compile('<MedeniHal>(.*?)</MedeniHal>', re.DOTALL)
        stil   = sablon.search(sVal)
        return stil.group(1)
    except: return '-1'

#-----------------------------------------------------------------------------
# Din kısmını getir
def getDin(sVal):
    try:
        sablon = re.compile('<Din>(.*?)</Din>', re.DOTALL)
        stil   = sablon.search(sVal)
        return stil.group(1)
    except: return '-1'

#-----------------------------------------------------------------------------
# Ölüm tarihi kısmını getir
def getOlumtarihi(sVal):
    try:
        sablon = re.compile('<OlumTarih><Yil>(.*?)</Yil><Ay>(.*?)</Ay><Gun>(.*?)</Gun></OlumTarih>', re.DOTALL)
        stil   = sablon.search(sVal)
        return stil.group(1) + "-" + stil.group(2)  + "-" + stil.group(3)
    except: return '-1'

#-----------------------------------------------------------------------------
# Ölüm yer kısmını getir
def getOlumyeri(sVal):
    try:
        sablon = re.compile('<OlumYer>(.*?)</OlumYer>', re.DOTALL)
        stil   = sablon.search(sVal)
        return stil.group(1)
    except: return '-1'

#-----------------------------------------------------------------------------
# İl kodu kısmını getir
def getIlkodu(sVal):
    try:
        sablon = re.compile('<IlKod>(.*?)</IlKod>', re.DOTALL)
        stil   = sablon.search(sVal)
        return stil.group(1)
    except: return '-1'

#-----------------------------------------------------------------------------
# İl Adı kısmını getir
def getIladi(sVal):
    try:
        sablon = re.compile('<IlAd>(.*?)</IlAd>', re.DOTALL)
        stil   = sablon.search(sVal)
        return stil.group(1)
    except: return '-1'

#-----------------------------------------------------------------------------
# İlçe kodu kısmını getir
def getIlcekodu(sVal):
    try:
        sablon = re.compile('<IlceKod>(.*?)</IlceKod>', re.DOTALL)
        stil   = sablon.search(sVal)
        return stil.group(1)
    except: return '-1'

#-----------------------------------------------------------------------------
# İlçe Adı kısmını getir
def getIlceadi(sVal):
    try:
        sablon = re.compile('<IlceAd>(.*?)</IlceAd>', re.DOTALL)
        stil   = sablon.search(sVal)
        return stil.group(1)
    except: return '-1'

#-----------------------------------------------------------------------------
# Cilt kodu kısmını getir
def getCiltkodu(sVal):
    try:
        sablon = re.compile('<CiltKod>(.*?)</CiltKod>', re.DOTALL)
        stil   = sablon.search(sVal)
        return stil.group(1)
    except: return '-1'

#-----------------------------------------------------------------------------
# Cilt Adı kısmını getir
def getCiltadi(sVal):
    try:
        sablon = re.compile('<CiltAd>(.*?)</CiltAd>', re.DOTALL)
        stil   = sablon.search(sVal)
        return stil.group(1)
    except: return '-1'

#-----------------------------------------------------------------------------
# Aile sıra no kısmını getir
def getAilesirano(sVal):
    try:
        sablon = re.compile('<AileSiraNo>(.*?)</AileSiraNo>', re.DOTALL)
        stil   = sablon.search(sVal)
        return stil.group(1)
    except: return '-1'

#-----------------------------------------------------------------------------
# Birey sıra no kısmını getir
def getBireysirano(sVal):
    try:
        sablon = re.compile('<BireySiraNo>(.*?)</BireySiraNo>', re.DOTALL)
        stil   = sablon.search(sVal)
        return stil.group(1)
    except: return '-1'

#-----------------------------------------------------------------------------
# XML Parse et
def XMLParse(sXmlVal):
    print sXmlVal
    HataKod = getHatakodu(sXmlVal)
    if HataKod != '0':
        print "Geçersiz Sorgulama" 
        sys.exit()
    SorguPozisyon = getSorgupozisyon(sXmlVal)
    TcKimlikno    = getTckimlikno(sXmlVal)
    ad            = getAd(sXmlVal)
    soyad         = getSoyad(sXmlVal)
    cinsiyet      = getCinsiyet(sXmlVal)
    BabaAd        = getBabaad(sXmlVal)
    BabaSoyad     = getBabasoyad(sXmlVal)
    AnaAd         = getAnaad(sXmlVal)
    AnaSoyad      = getAnasoyad(sXmlVal)
    DogumTarihi   = getDogumtarihi(sXmlVal)
    DogumYeri     = getDogumyeri(sXmlVal)
    KizlikSoyadi  = getKizliksoyadi(sXmlVal)
    OzurOran      = getOzuroran(sXmlVal)
    durum         = getDurum(sXmlVal)
    MedeniHal     = getMedenihal(sXmlVal)
    Din           = getDin(sXmlVal)
    OlumTarihi    = getOlumtarihi(sXmlVal)
    OlumYeri      = getOlumyeri(sXmlVal)
    IlKodu        = getIlkodu(sXmlVal)
    IlAdi         = getIladi(sXmlVal)
    IlceKodu      = getIlcekodu(sXmlVal)
    IlceAdi       = getIlceadi(sXmlVal)
    CiltKodu      = getCiltkodu(sXmlVal)
    CiltAdi       = getCiltadi(sXmlVal)
    AileSiraNo    = getAilesirano(sXmlVal)
    BireySiraNo   = getBireysirano(sXmlVal)
    print """
            HataKod         = %s
            SorguPozisyon   = %s
            Tckimlikno      = %s
            Ad              = %s
            Soyad           = %s
            cinsiyet        = %s
            Baba Adı        = %s
            Baba Soyadı     = %s
            Ana Adı         = %s
            Ana Soyad       = %s
            Doğum Tarihi    = %s
            Doğum Yeri      = %s
            Kızlık Soyadi   = %s
            Özür Oran       = %s
            Durum           = %s
            Medeni Hal      = %s
            Din             = %s
            Ölüm Tarihi     = %s
            Ölüm Yeri       = %s
            İl Kodu         = %s
            İl Adi          = %s
            İlçe Kodu       = %s
            İlçe Adi        = %s
            Cilt Kodu       = %s
            Cilt Adı        = %s
            Aile Sıra No    = %s
            Birey Sıra No   = %s
          """ % (HataKod, SorguPozisyon, TcKimlikno, ad, soyad, cinsiyet,
                BabaAd, BabaSoyad, AnaAd, AnaSoyad, DogumTarihi, DogumYeri,
                KizlikSoyadi, OzurOran, durum, MedeniHal, Din, OlumTarihi,
                OlumYeri, IlKodu, IlAdi, IlceKodu, IlceAdi, CiltKodu, 
                CiltAdi, AileSiraNo, BireySiraNo)

#-----------------------------------------------------------------------------
# Proses buradan başlıyor      
if __name__ == "__main__":     
    vRndnum,vNonce,vTimestamp,vCreated,vExpires,vParola = getVariable()
    msg     = getMsg(TCKIMLIKNO,vNonce,vCreated,vExpires,USERNAME, vParola)
    body    = msg 
                  
    headers =  [  
                "User-Agent: python",
                "Content-Type: text/xml; charset=utf-8",
                'SOAPAction: "http://kps.nvi.gov.tr/WS/TCKimlikNodanKisiBilgisiSorgula"'
               ]  
    SIO    = StringIO.StringIO()  
    try:          
        ch     = pycurl.Curl() 
        ch.setopt(ch.URL,WSDL_URL)
        ch.setopt(ch.FOLLOWLOCATION, True)
        ch.setopt(ch.HEADER,True) 
        #ch.setopt(ch.RETURNTRANSFER, 1)
        ch.setopt(ch.TIMEOUT, 30) 
        ch.setopt(ch.SSL_VERIFYPEER, False)
        ch.setopt(ch.SSL_VERIFYHOST, False)
        ch.setopt(ch.HTTPHEADER,headers)
        ch.setopt(ch.POST,True)
        ch.setopt(ch.POSTFIELDS,body)
        ch.setopt(ch.WRITEFUNCTION, SIO.write)
        ch.perform()           
        ch.close()
    except:
        print "Bağlantı hatası"
        sys.exit()
    xmlval = SIO.getvalue()    
    XMLParse(xmlval)           
    #print XMLVal