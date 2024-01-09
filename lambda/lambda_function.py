#GET_Node-Red

URL = "https://note.convergedigital.com.br/get"
USUARIO = "carlos"
SENHA = "261297"

import requests
import json
import logging
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model.slu.entityresolution.resolution import Resolution
from ask_sdk_model.slu.entityresolution import StatusCode
from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_request_type("LaunchRequest")(handler_input)
        
    def handle(self, handler_input):
        
        PE = (requests.get(URL, auth=(USUARIO, SENHA), headers={'content-type': 'text/plain'})).text
        
        return (
            handler_input.response_builder
                .speak(PE)
                .ask(PE)
                .response
        )

class IntencaoDeComandoIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name('intencao_de_comando')(handler_input)
        
    def handle(self, handler_input):
        slot = ask_utils.get_slot(handler_input=handler_input, slot_name="comando_selecionado")
        
        if slot and slot.resolutions and slot.resolutions.resolutions_per_authority:
            for resolution in slot.resolutions.resolutions_per_authority:
                if resolution.status.code == StatusCode.ER_SUCCESS_MATCH:
                    
                    requests.post(URL, auth=(USUARIO, SENHA), json = {'comando': resolution.values[0].value.name, 'pergunta': (requests.get(URL, auth=(USUARIO, SENHA), headers={'content-type': 'text/plain'})).text, 'dispositivo': handler_input.request_envelope.context.system.device.device_id})
                    
                else:
                    raise
                
        return (
            handler_input.response_builder
                .speak("Okey.")
                .response
        )

class CancelIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input)
        
    def handle(self, handler_input):
        
        requests.post(URL, auth=(USUARIO, SENHA), json = {'comando': "Solicitação de cancelamento", 'pergunta': (requests.get(URL, auth=(USUARIO, SENHA), headers={'content-type': 'text/plain'})).text, 'dispositivo': handler_input.request_envelope.context.system.device.device_id})
        
        return (
            handler_input.response_builder
                .speak("Okey.")
                .response
        )
    
class StopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input)
        
    def handle(self, handler_input):
        
        requests.post(URL, auth=(USUARIO, SENHA), json = {'comando': "Solicitação de parada", 'pergunta': (requests.get(URL, auth=(USUARIO, SENHA), headers={'content-type': 'text/plain'})).text, 'dispositivo': handler_input.request_envelope.context.system.device.device_id})
        
        return (
            handler_input.response_builder
                .speak("Okey.")
                .response
        )

class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)
        
    def handle(self, handler_input):
        
        requests.post(URL, auth=(USUARIO, SENHA), json = {'comando': "Solicitação de ajuda", 'pergunta': (requests.get(URL, auth=(USUARIO, SENHA), headers={'content-type': 'text/plain'})).text, 'dispositivo': handler_input.request_envelope.context.system.device.device_id})
        
        return (
            handler_input.response_builder
                .speak("Não posso fornecer ajuda. Tente outra vez.")
                .ask("Não tenho instruções para suporte. Tente outra vez.")
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)
        
    def handle(self, handler_input):
        logger.info("In FallbackIntentHandler")
        
        requests.post(URL, auth=(USUARIO, SENHA), json = {'comando': "Não compreendido", 'pergunta': (requests.get(URL, auth=(USUARIO, SENHA), headers={'content-type': 'text/plain'})).text, 'dispositivo': handler_input.request_envelope.context.system.device.device_id})
        
        return (
            handler_input.response_builder
                .speak("Não entendi corretamente. Pode repetir?")
                .ask("Realmente não entendi. Tente outra vez.")
                .response
        )

class EndedRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)
        
    def handle(self, handler_input):
        
        requests.post(URL, auth=(USUARIO, SENHA), json = {'comando': "Não houve resposta", 'pergunta': (requests.get(URL, auth=(USUARIO, SENHA), headers={'content-type': 'text/plain'})).text, 'dispositivo': handler_input.request_envelope.context.system.device.device_id})
            
        return (
            handler_input.response_builder
                .response
        )
    
class CatchAllExceptionHandler(AbstractExceptionHandler):
    def can_handle(self, handler_input, exception):
        return True
            
    def handle(self, handler_input, exception):
        logger.error(exception, exc_info=True)
        
        requests.post(URL, auth=(USUARIO, SENHA), json = {'comando': "Resposta não incluída", 'pergunta': (requests.get(URL, auth=(USUARIO, SENHA), headers={'content-type': 'text/plain'})).text, 'dispositivo': handler_input.request_envelope.context.system.device.device_id})
        
        return (
            handler_input.response_builder
                .speak("Não inserida.")
                .ask("Resposta não incluída.")
                .response
        )

sb = SkillBuilder()
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(IntencaoDeComandoIntentHandler())
sb.add_request_handler(CancelIntentHandler())
sb.add_request_handler(StopIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(EndedRequestHandler())
sb.add_exception_handler(CatchAllExceptionHandler())
lambda_handler = sb.lambda_handler()