import json
from pathlib import Path
import pytest
from infrastructure.database.engine import Database
from integrations.alibaba.contract_validator import AlibabaContractValidator,ContractValidationError
from integrations.alibaba.request_audit import redact
from integrations.carriers.delivery_estimator import DeliveryEstimator
from integrations.email.template_renderer import TemplateRenderer
from integrations.shopify.graphql_document_loader import GraphQLDocumentLoader
from integrations.shopify.graphql_response_validator import GraphqlResponseValidator,ShopifyGraphqlResponseError
from integrations.shopify.bulk.jsonl_stream_reader import JsonlStreamReader
from integrations.tax.static_tax_provider import StaticTaxProvider


def test_all_graphql_documents_are_named_and_loadable():
    root=Path('integrations/shopify/operations');loader=GraphQLDocumentLoader(root)
    files=list(root.rglob('*.graphql'));assert len(files)>=60
    for path in files: assert loader.load(str(path.relative_to(root))).split()[0] in {'query','mutation','subscription'}

def test_alibaba_contract_validator():
    validator=AlibabaContractValidator();assert validator.validate('order_status',{'orderId':'1','status':'paid'})['status']=='paid'
    with pytest.raises(ContractValidationError):validator.validate('order_status',{'orderId':'1'})

def test_request_audit_redacts_nested_secret():
    assert redact({'x':{'access_token':'abc'}})['x']['access_token']=='***'

def test_jsonl_reader_is_streaming(tmp_path):
    path=tmp_path/'x.jsonl';path.write_text('{"id":1}\n{"id":2}\n',encoding='utf-8');assert [x['id'] for x in JsonlStreamReader().read(path)]==[1,2]

def test_response_validator_rejects_graphql_errors():
    with pytest.raises(ShopifyGraphqlResponseError):GraphqlResponseValidator().validate({'errors':[{'message':'x'}]})

def test_template_renderer_and_delivery_estimate():
    assert TemplateRenderer().render('Bonjour {{ customer.name }}',{'customer':{'name':'Ada'}})=='Bonjour Ada'
    assert DeliveryEstimator().estimate(__import__('datetime').date(2026,1,1),2,5)['window_days']==5

@pytest.mark.asyncio
async def test_static_tax_provider():
    quote=await StaticTaxProvider({'CA:QC':.14975}).quote(100,'CA','QC');assert quote.tax==14.98 and quote.total==114.98
