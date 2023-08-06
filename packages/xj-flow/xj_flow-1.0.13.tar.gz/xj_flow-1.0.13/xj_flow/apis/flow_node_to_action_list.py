# _*_coding:utf-8_*_

from rest_framework.views import APIView

from ..services.flow_basic_service import FlowBasicService
from ..utils.custom_response import util_response
from ..utils.custom_tool import format_params_handle
from ..utils.request_params_wrapper import request_params_wrapper


class FlowNodeToActionList(APIView):
    @request_params_wrapper
    def get(self, *args, request_params=None, **kwargs):
        """
        流程作业
        """
        if request_params is None:
            request_params = {}
        need_custom_serialize = request_params.pop("need_custom_serialize", None)
        request_params = format_params_handle(
            param_dict=request_params,
            filter_filed_list=["flow_id", "flow_node_id", "flow_action_id", "flow_node_value", "flow_action", "flow_status_code_list"],
            split_list=["flow_status_code_list"],
            is_remove_empty=True
        )

        need_custom_serialize = need_custom_serialize == 1 or need_custom_serialize == True or need_custom_serialize == "1" or need_custom_serialize == "true"
        flow_list, error_text = FlowBasicService.get_flow_node_to_action_list(params=request_params, need_custom_serialize=need_custom_serialize)
        return util_response(data=flow_list)
