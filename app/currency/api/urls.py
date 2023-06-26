from rest_framework.routers import DefaultRouter

from currency.api.views import (ContactUsApiViewSet,
                                RateApiViewSet,
                                RequestResponseLogApiViewSet,
                                SourceApiViewSet)

app_name = 'api-currency'

router = DefaultRouter()
router.register(r'rates', RateApiViewSet, basename='rates')
router.register(r'sources', SourceApiViewSet, basename='sources')
router.register(r'feedbacks', ContactUsApiViewSet, basename='feedbacks')
router.register(r'logs', RequestResponseLogApiViewSet, basename='logs')
urlpatterns = router.urls
