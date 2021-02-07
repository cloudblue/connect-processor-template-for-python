from connect.resources import TierConfigAutomation
from connect.models import ActivationTemplateResponse, Param, TierConfigRequest
# from app.utils.logger import logger, function_log
from app.utils.utils import Utils
from connect.exceptions import FailRequest, SkipRequest, InquireRequest
from app.utils.message import Message
from app.utils.globals import Globals

# class TierConfiguration(TierConfigAutomation):

    # @function_log
    # def process_request(self, tier_request: TierConfigRequest):
    #     try:

            # logger.info(
            #     f"##### Processing Tier Config Request: {tier_request.id} for tier configuration: {tier_request.configuration.id} starts. ########")
            # logger.debug(f"TierConfigurationRequest: {Utils.serialize(tier_request)}")


        # except Exception as ex:
            # logger.error(
            #     Globals.SKIP_ACTION + Message.Shared.tier_request.ERROR_PROCESSING_TIER_REQUEST.format(str(ex)))
            # raise SkipRequest(Message.Shared.tier_request.ERROR_PROCESSING_TIER_REQUEST.format(str(ex)))