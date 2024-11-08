from django.views import View

from MaxPainChartingService import MaxPainChartingService
from django.http import JsonResponse

class MaxPainChartingAPI(View):
    def __init__(self, **kwargs):
        self.service = MaxPainChartingService()
        super().__init__(**kwargs)
    
    def get_ticker_details(self):
        details, err = self.service.get_ticker_details()

        if err:
            return JsonResponse({"error" : err}, status=400) 
        
        return JsonResponse(details, status=200)

        




