from ninja import NinjaAPI
apiv1 = NinjaAPI()

@apiv1.get('hello/')
def helloApi(request):
    return "Menyala abangkuh ..."