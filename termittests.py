

import requests
import json
import os
import requests.exceptions
import sys

TERMITUP_URL='http://localhost:80'

#test terminology extraction#
def test_module1():
    url_request= TERMITUP_URL+ '/extract_terminology'
    print('URL:')
    print(url_request)
    text=''' "Como muchos grupos y personas creen que sus sistemas políticos no responden a sus demandas políticas, recurren a uno de los Derechos del hombre reconocidos, implícitamente, en la Declaración de Independencia de los Estados Unidos (1776) y, explícitamente, en las Constituciones de la Revolución Francesa de 1789 y 1793, el de Resistencia a la opresión, para cambiar la forma de gobierno en todo o en parte (alguna disposición concreta) por medio de acciones de fuerza. Es, pues, una forma de activismo, propaganda, presión o persuasión entre muchos otros menos discutibles según criterios éticos, como la desobediencia civil o la no violencia.

Han estudiado el papel de la violencia política en la historia teólogos, filósofos, historiadores, politólogos y sociólogos como Tomás de Aquino, que autorizó en el siglo XIII el levantamiento popular contra los gobiernos tiránicos y en el siglo XVI, Nicolás Maquiavelo, para quien la razón de estado justifica a veces realizar el mal menor para evitar el mal mayor y la crueldad puede estar justificada en un buen gobierno, ya que la política es una realidad ajena a toda moral, si es que es a hombres a los que hay que gobernar. En el siglo XIX, Karl Marx afirmaba que la violencia es la comadrona de la Historia y por lo tanto está autorizada por la lucha de clases y el materialismo histórico, y su amigo y seguidor Friedrich Engels escribió al respecto un ensayo no concluido, El papel de la violencia en la Historia (1888). También estudió este fenómeno el sociólogo Georges Sorel en sus Reflexiones sobre la violencia (1908), autorizando en cierta manera el Terrorismo de fin político y social. La legitimidad de la acción política violenta la ofrece a posteriori el éxito de la misma. Como escribió Pedro Calderón de la Barca en su La vida es sueño, cuando en la tercera jornada estalla la guerra civil, batallas tales / quienes vencen son leales / los vencidos, los traidores.

Como resultado, personas, grupos, religiones y algunos regímenes políticos suelen creer que algunos o todos los distintos tipos de violencia política no solo están justificados, sino que son necesarios para lograr objetivos políticos y algunos gobiernos los utilizan para intimidar a sus poblaciones e inclinarlas a la aquiescencia. La inacción o pasividad de un gobierno también puede ser tomada como una forma de violencia política, por ejemplo cuando, en vísperas de la Guerra Civil Española, el Gobierno republicano adoptó una actitud de no intervención ante el incendio y pillaje de iglesias y, posteriormente, no reprimió sino muy tarde los actos violentos de los grupos paramilitares comunistas y anarquistas que se levantaron contra los levantados y a los que ella misma permitió que se les diesen armas. En el curso de la historia, el siglo XX ha sido probablemente el siglo con más violencia de esta clase que ha existido nunca. Sin embargo, al menos en el campo de la izquierda, hubo un Revisionismo de la filosofía política marxista por parte de Eduard Bernstein y Jean Jaurès que excluyó la idea de la revolución violenta para alcanzar el socialismo y optó por la evolución para llegar a él mediante el sindicalismo y la acción política.",
'''    
	
    data={
	"corpus": text,
    "language":"es"
    
	}
	
        
    # Do a Post         
    response = requests.post(url_request, json=data)

    print(response.content)
    print(response)




def test_module2():
    url_request= TERMITUP_URL+ '/postproc_terminology'
    print('URL:')
    print(url_request)
  	
    data={
	"terms": "ley, orden, cabeza, octubre, de, los, pepino, otros, tuyos",
    "language":"es"
    
	}
	
        
    # Do a Post         
    response = requests.post(url_request, json=data)

    print(response.content)
    print(response)


#test_module1()
test_module2()
