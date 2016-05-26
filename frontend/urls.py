from django.conf import settings
from django.conf.urls import patterns, url, include
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.views.generic import ListView, DetailView
from django.views.generic.base import TemplateView
#from django.views.generic.simple import direct_to_template
from django.views.decorators.csrf import csrf_exempt

from regluit.core.feeds import SupporterWishlistFeed
from regluit.core.models import Campaign
from regluit.frontend.views import (
    GoodreadsDisplayView,
    LibraryThingView,
    PledgeView,
    PurchaseView,
    FundCompleteView,
    PledgeCancelView,
    PledgeRechargeView,
    FAQView,
    CampaignListView,
    WorkListView,
    UngluedListView,
    InfoPageView,
    InfoLangView,
    GiftView,
    FundView,
    NonprofitCampaign,
    GiftCredit,
    PledgeModifiedView,
    ManageAccount,
    MergeView,
    ByPubListView,
    ByPubView,
    kindle_config,
    send_to_kindle,
    LibModeView,
    DownloadView,
    FacetedView,
    MapSubjectView,
)

urlpatterns = patterns(
    "regluit.frontend.views",
    url(r"^$", "home", name="home"),
    url(r"^landing/$", "home", {'landing': True}, name="landing"),
    url(r"^next/$", "next", name="next"),
    url(r"^supporter/(?P<supporter_username>[^/]+)/$", "supporter", {'template_name': 'supporter.html'}, name="supporter"),
    url(r"^supporter/(?P<userlist>[^/]+)/marc/$", "userlist_marc", name="user_marc"),
    url(r"^library/(?P<library_name>[^/]+)/$", "library", name="library"),
    url(r"^accounts/manage/$", login_required(ManageAccount.as_view()), name="manage_account"),
    url(r"^search/$", "search", name="search"),
    url(r"^privacy/$", TemplateView.as_view(template_name="privacy.html"),
        name="privacy"),
    url(r"^terms/$", TemplateView.as_view(template_name="terms.html"),
        name="terms"),
    url(r"^rightsholders/$", "rh_tools", name="rightsholders"), 
    url(r"^rightsholders/campaign/(?P<id>\d+)/$", "manage_campaign", name="manage_campaign"), 
    url(r"^rightsholders/campaign/(?P<id>\d+)/results/$", "manage_campaign", {'action': 'results'}, name="campaign_results"), 
    url(r"^rightsholders/campaign/(?P<id>\d+)/makemobi/$", "manage_campaign", {'action': 'makemobi'}, name="makemobi"),
    url(r"^rightsholders/campaign/(?P<id>\d+)/mademobi/$", "manage_campaign", {'action': 'mademobi'}, name="mademobi"),
    url(r"^rightsholders/edition/(?P<work_id>\d*)/(?P<edition_id>\d*)$", "new_edition",{'by': 'rh'}, name="rh_edition"),
    url(r"^rightsholders/edition/(?P<edition_id>\d*)/upload/$", "edition_uploads", name="edition_uploads"),
    url(r"^rightsholders/claim/$", "claim", name="claim"), 
    url(r"^rightsholders/surveys/$", "surveys", name="surveys"), 
    url(r"^rightsholders/new_survey/(?P<work_id>\d*)/?$", "new_survey", name="new_survey"),
    url(r"^rh_admin/$", "rh_admin", name="rh_admin"),
    url(r"^rh_admin/accepted/$", "rh_admin", {'facet': 'accepted'}, name="accepted"),
    url(r"^rh_admin/claims/$", "rh_admin", {'facet': 'claims'}, name="claims"),
    url(r"^campaign_admin/$", "campaign_admin", name="campaign_admin"),    
    url(r"^faq/$", FAQView.as_view(), {'location':'faq', 'sublocation':'all'}, name="faq"), 
    url(r"^faq/(?P<location>\w*)/$", FAQView.as_view(), {'sublocation':'all'}, name="faq_location"), 
    url(r"^faq/(?P<location>\w*)/(?P<sublocation>\w*)/$", FAQView.as_view(), name="faq_sublocation"), 
    url(r"^wishlist/$", "wishlist", name="wishlist"),
    url(r"^msg/$", "msg", name="msg"),
    url(r"^campaigns/(?P<facet>\w*)$", CampaignListView.as_view(), name='campaign_list'),
    url(r"^campaigns/(?P<facet>\w*)/marc/$", CampaignListView.as_view(send_marc=True), name='campaign_list_marc'),
    url(r"^lists/(?P<facet>\w*)$", WorkListView.as_view(),  name='work_list'),
    url(r"^lists/(?P<facet>\w*)/marc/$", WorkListView.as_view(send_marc=True),  name='work_list_marc'),
    url(r"^free/(?P<path>.*)/marc/$", FacetedView.as_view(send_marc=True),  name='faceted_list_marc'),
    url(r"^free/(?P<path>.*)/$", FacetedView.as_view(),  name='faceted_list'),
    url(r"^free/$", FacetedView.as_view(),  name='free'),
    url(r"^pid/all/(?P<pubname>\d+)$", ByPubView.as_view(),  name='bypubname_list'),
    url(r"^pid/(?P<facet>\w*)/(?P<pubname>\d+)$", ByPubView.as_view(),  name='bypubname_list'),
    url(r"^pid/(?P<facet>\w*)/(?P<pubname>\d+)/marc/$", ByPubView.as_view(send_marc=True),  name='bypubname_list_marc'),
    url(r"^bypub/all/(?P<pubname>.*)$", ByPubListView.as_view(),  name='bypub_list'),
    url(r"^bypub/(?P<facet>\w*)/(?P<pubname>.*)$", ByPubListView.as_view(),  name='bypub_list'),
    url(r"^unglued/(?P<facet>\w*)$", UngluedListView.as_view(),  name='unglued_list'),
    url(r"^unglued/(?P<facet>\w*)/marc/$", UngluedListView.as_view(send_marc=True),  name='unglued_list_marc'),
    url(r"^creativecommons/$", FacetedView.as_view(),  name='cc_list'),
    url(r"^creativecommons/(?P<path>[^\s]*)/marc/$", FacetedView.as_view(send_marc=True),  name='cc_list_marc'),
    url(r"^creativecommons/(?P<path>[^\s]*)$", FacetedView.as_view(),  name='cc_list_detail'),
    url(r"^goodreads/auth/$", "goodreads_auth", name="goodreads_auth"),
    url(r"^goodreads/auth_cb/$", "goodreads_cb", name="goodreads_cb"),
    url(r"^goodreads/flush/$","goodreads_flush_assoc", name="goodreads_flush_assoc"),
    url(r"^goodreads/load_shelf/$","goodreads_load_shelf", name="goodreads_load_shelf"),
    url(r"^goodreads/shelves/$","goodreads_calc_shelves", name="goodreads_calc_shelves"),
    url(r"^stub/", "stub", name="stub"),
    url(r"^work/(?P<work_id>\d+)/$", "work", name="work"),
    url(r"^work/(?P<work_id>\d+)/preview/$", "work", {'action': 'preview'}, name="work_preview"),
    url(r"^work/(?P<work_id>\d+)/acks/$", "work", {'action': 'acks'}, name="work_acks"),
    url(r"^work/(?P<work_id>\d+)/lockss/$", "lockss", name="lockss"),
    url(r"^lockss/(?P<year>\d+)/$", "lockss_manifest", name="lockss_manifest"),
    url(r"^work/(?P<work_id>\d+)/download/$", DownloadView.as_view(), name="download"),
    url(r"^work/(?P<work_id>\d+)/download/$", DownloadView.as_view(), name="thank"),
    url(r"^work/(?P<work_id>\d+)/unglued/(?P<format>\w+)/$", "download_campaign", name="download_campaign"),
    url(r"^work/(?P<work_id>\d+)/borrow/$", "borrow", name="borrow"),
    url(r"^work/(?P<work_id>\d+)/marc/$", "work_marc", name="work_marc"),
    url(r"^work/(?P<work_id>\d+)/reserve/$", "reserve", name="reserve"),
    url(r"^work/(?P<work_id>\d+)/feature/$", "feature", name="feature"),
    url(r"^work/(?P<work_id>\d+)/kw/$", "kw_edit", name="kw_edit"),
    url(r"^work/(?P<work_id>\d+)/merge/$", login_required(MergeView.as_view()), name="merge"),
    url(r"^work/(?P<work_id>\d+)/editions/$", "work",{'action': 'editions'}, name="work_editions"),
    url(r"^work/\d+/acks/images/(?P<file_name>[\w\.]*)$", "static_redirect_view",{'dir': 'images'}), 
    url(r"^work/(?P<work_id>\d+)/librarything/$", "work_librarything", name="work_librarything"),
    url(r"^work/(?P<work_id>\d+)/goodreads/$", "work_goodreads", name="work_goodreads"),
    url(r"^work/(?P<work_id>\d+)/openlibrary/$", "work_openlibrary", name="work_openlibrary"),
    url(r"^new_edition/(?P<work_id>)(?P<edition_id>)$", "new_edition", name="new_edition"),
    url(r"^new_edition/(?P<work_id>\d*)/(?P<edition_id>\d*)$", "new_edition", name="new_edition"),
    url(r"^manage_ebooks/(?P<edition_id>\d*)$", "manage_ebooks", name="manage_ebooks"),
    url(r"^googlebooks/(?P<googlebooks_id>.+)/$", "googlebooks", name="googlebooks"),
    url(r"^download_ebook/(?P<ebook_id>\w+)/$", "download_ebook", name="download_ebook"),
    url(r"^download_ebook/acq/(?P<format>\w+)/(?P<nonce>\w+)/$", "download_acq", name="download_acq"),
    url(r"^receive_gift/(?P<nonce>\w+)/$", "receive_gift", name="receive_gift"),
    url(r"^display_gift/(?P<gift_id>\d+)/(?P<message>newuser|existing)/$", "display_gift", name="display_gift"),
    url(r"^gift/$", login_required(GiftView.as_view()), name="gift"),
    url(r"^gift/credit/(?P<token>.+)/$", login_required(GiftCredit.as_view()), name="gift_credit"),
    url(r"^pledge/(?P<work_id>\d+)/$", login_required(PledgeView.as_view(),login_url='/accounts/login/pledge/'), name="pledge"),
    url(r"^pledge/cancel/(?P<campaign_id>\d+)$", login_required(PledgeCancelView.as_view()), name="pledge_cancel"),
    url(r"^fund/complete/$", FundCompleteView.as_view(), name="pledge_complete"),
    url(r"^pledge/modified/$", login_required(PledgeModifiedView.as_view()), name="pledge_modified"),
    url(r"^pledge/modify/(?P<work_id>\d+)$", login_required(PledgeView.as_view()), name="pledge_modify"),
    url(r"^payment/fund/(?P<t_id>\d+)$", FundView.as_view(), name="fund" ),
    url(r"^pledge/recharge/(?P<work_id>\d+)$", login_required(PledgeRechargeView.as_view()), name="pledge_recharge"),
    url(r"^purchase/(?P<work_id>\d+)/$", login_required(PurchaseView.as_view(),login_url='/accounts/login/purchase/'), name="purchase"),
    url(r"^purchase/(?P<work_id>\d+)/download/$", "download_purchased", name="download_purchased"),
    url(r"^donate_to_campaign/$", csrf_exempt(NonprofitCampaign.as_view()), name="nonprofit"),
    url(r"^subjects/$", "subjects", name="subjects"),
    url(r"^subjects/map/$", login_required(MapSubjectView.as_view()), name="map_subject"),
    url(r"^librarything/$", LibraryThingView.as_view(), name="librarything"),
    url(r"^librarything/load/$","librarything_load", name="librarything_load"),
    url('^404testing/$', TemplateView.as_view(template_name='404.html') ),
    url('^500testing/$', TemplateView.as_view(template_name='500.html')),
    url('^robots.txt$', TemplateView.as_view(template_name='robots.txt',content_type='text/plain')),
    url(r"^emailshare/(?P<action>\w*)/?$", "emailshare", name="emailshare"),
    url(r"^feedback/campaign/(?P<campaign_id>\d+)/?$", "ask_rh", name="ask_rh"),
    url(r"^feedback/$", "feedback", name="feedback"),
    url(r"^feedback/thanks/$", TemplateView.as_view(template_name="thanks.html")),
    url(r"^about/$", TemplateView.as_view(template_name="about.html"),
        name="about"),
    url(r"^comments/$", "comment", name="comment"),
    url(r"^info/(?P<template_name>[\w\.]*)$", InfoPageView.as_view()), 
    url(r"^info/languages/(?P<template_name>[\w\.]*)$", InfoLangView.as_view()), 
    url(r'^supporter/(?P<supporter>[^/]+)/feed/$', SupporterWishlistFeed()),
    url(r'^campaign_archive.js/$', "campaign_archive_js", name="campaign_archive_js"),
    url(r"^about/(?P<facet>\w*)/$", "about",  name="about_specific"),
    url(r"^libraries/$", TemplateView.as_view(
            template_name="libraries.html",
            get_context_data=lambda: {'site': Site.objects.get_current()}
        ),
        name="libraries"),
    url(r"^ml/status/$","ml_status",  name="ml_status"),
    url(r"^ml/subscribe/$","ml_subscribe",  name="ml_subscribe"),
    url(r"^ml/unsubscribe/$","ml_unsubscribe",  name="ml_unsubscribe"),
    url(r"^press/$","press",  name="press"),
    url(r"^press_submitterator/$","press_submitterator",  name="press_submitterator"),
    url(r"^accounts/edit/kindle_config/$", "kindle_config",  name="kindle_config"),
    url(r"^accounts/edit/kindle_config/(?P<work_id>\d+)/$", "kindle_config",  name="kindle_config_download"),
    url(r"^send_to_kindle/(?P<work_id>\d+)/(?P<javascript>\d)/$", "send_to_kindle",  name="send_to_kindle"),
    url(r"^marc/$", TemplateView.as_view(template_name='marc.html'), name="marc"),
    url(r"^accounts/edit/marc_config/$", login_required(LibModeView.as_view()),  name="marc_config"),
    
)

if settings.DEBUG:
    urlpatterns += patterns(
        "regluit.frontend.views",
        url(r"^goodreads/$", login_required(GoodreadsDisplayView.as_view()), name="goodreads_display"),
        url(r"^goodreads/clear_wishlist/$","clear_wishlist", name="clear_wishlist"),
        url(r"^celery/clear/$","clear_celery_tasks", name="clear_celery_tasks"),
)