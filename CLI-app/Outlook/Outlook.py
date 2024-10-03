import asyncio
import configparser
from msgraph.generated.models.o_data_errors.o_data_error import ODataError
from configparser import SectionProxy
from azure.identity import DeviceCodeCredential
from msgraph import GraphServiceClient
from msgraph.generated.users.item.user_item_request_builder import UserItemRequestBuilder
from msgraph.generated.users.item.mail_folders.item.messages.messages_request_builder import MessagesRequestBuilder
from msgraph.generated.users.item.send_mail.send_mail_post_request_body import SendMailPostRequestBody
from msgraph.generated.models.message import Message
from msgraph.generated.models.item_body import ItemBody
from msgraph.generated.models.body_type import BodyType
from msgraph.generated.models.recipient import Recipient
from msgraph.generated.models.email_address import EmailAddress
import time

#TODO: Two time first login (seems greet user asks for it and the login beforehand also asks, if this doesnt occur then it requires you to login twice through the CLI menu)
#TODO: Change from access token to refresh token
#TODO: Modularise code to make it useable and accessible
#TODO: Adhere to Email datatype, grab relevant information from email so it can be used in the rest of the software


class Outlook:

    settings:               SectionProxy
    device_code_credential: DeviceCodeCredential
    user_client:            GraphServiceClient
    access_token:           str
    token_expiry:           float

    def __init__(self, config: SectionProxy):

        self.settings = config

        client_id = self.settings['clientId'] # Application ID 
        tenant_id = self.settings['tenantId'] # User type

        graph_scopes = self.settings['graphUserScopes'].split(' ')

        self.device_code_credential = DeviceCodeCredential(client_id, tenant_id=tenant_id)
        self.user_client = GraphServiceClient(self.device_code_credential, graph_scopes)

        self.access_token = None
        self.token_expiry = 0

    async def get_user_token(self):

        # Check if the current token is still valid
        if self.access_token is None or time.time() >= self.token_expiry:
            graph_scopes = self.settings['graphUserScopes']
            token_response = self.device_code_credential.get_token(graph_scopes)  # this is where the access token is actually used (passed to)
            self.access_token = token_response.token
            self.token_expiry = time.time() + token_response.expires_on - 60  # Refresh 1 minute before expiry

       

    async def get_user(self):
        await self.get_user_token()
        query_params = UserItemRequestBuilder.UserItemRequestBuilderGetQueryParameters(
            select=['displayName', 'mail', 'userPrincipalName']
        )
        request_config = UserItemRequestBuilder.UserItemRequestBuilderGetRequestConfiguration(
            query_parameters=query_params
        )

        user = await self.user_client.me.get(request_configuration=request_config)
        return user

    async def get_inbox(self):

        await self.get_user_token()

        query_params = MessagesRequestBuilder.MessagesRequestBuilderGetQueryParameters(
            select=['from', 'isRead', 'receivedDateTime', 'subject'],
            top=25,
            orderby=['receivedDateTime DESC']
        )
        request_config = MessagesRequestBuilder.MessagesRequestBuilderGetRequestConfiguration(
            query_parameters=query_params
        )

        messages = await self.user_client.me.mail_folders.by_mail_folder_id('inbox').messages.get(
            request_configuration=request_config)
        return messages

    async def send_mail(self, subject: str, body: str, recipient: str):
        token = await self.get_user_token()
        message = Message()
        message.subject = subject

        message.body = ItemBody()
        message.body.content_type = BodyType.Text
        message.body.content = body

        to_recipient = Recipient()
        to_recipient.email_address = EmailAddress()
        to_recipient.email_address.address = recipient
        message.to_recipients = []
        message.to_recipients.append(to_recipient)

        request_body = SendMailPostRequestBody()
        request_body.message = message

        await self.user_client.me.send_mail.post(body=request_body)


async def main():
    config = configparser.ConfigParser()
    config.read(['Outlook/config.cfg', 'Outlook/config.dev.cfg'])
    azure_settings = config['azure']

    graph: Outlook = Outlook(azure_settings)

    await greet_user(graph)

    choice = -1

    while choice != 0:
        print('Please choose one of the following options:')
        print('0. Exit')
        print('1. Display access token')
        print('2. List my inbox')
        print('3. Send mail')
        print('4. Make a Graph call')

        try:
            choice = int(input())
        except ValueError:
            choice = -1

        try:
            if choice == 0:
                print('Goodbye...')
            elif choice == 1:
                await display_access_token(graph)
            elif choice == 2:
                await list_inbox(graph)
            elif choice == 3:
                await send_mail(graph)
            elif choice == 4:
                await make_graph_call(graph)
            else:
                print('Invalid choice!\n')
        except ODataError as odata_error:
            print('Error:')
            if odata_error.error:
                print(odata_error.error.code, odata_error.error.message)


async def greet_user(graph: Outlook):
    user = await graph.get_user()
    if user:
        print('Hello,', user.display_name)
        print('Email:', user.mail or user.user_principal_name, '\n')

async def display_access_token(graph: Outlook):
    token = await graph.get_user_token()
    print('User token:', token, '\n')

async def list_inbox(graph: Outlook):
    message_page = await graph.get_inbox()
    if message_page and message_page.value:
        for message in message_page.value:
            print('Message:', message.subject)
            if message.from_ and message.from_.email_address:
                print('  From:', message.from_.email_address.name or 'NONE')
            else:
                print('  From: NONE')
            print('  Status:', 'Read' if message.is_read else 'Unread')
            print('  Received:', message.received_date_time)

        more_available = message_page.odata_next_link is not None
        print('\nMore messages available?', more_available, '\n')

async def send_mail(graph: Outlook):
    user = await graph.get_user()
    if user:
        user_email = user.mail or user.user_principal_name
        await graph.send_mail('Testing Microsoft Graph', 'Hello world!', user_email or '')
        print('Mail sent.\n')


asyncio.run(main())
