from django.shortcuts import render,redirect
from django.views import View

#クエリビルダ(複雑な検索処理を行う事ができる)
from django.db.models import Q


from .models import Medicine

class IndexView(View):

    def get(self, request, *args, **kwargs):

        #検索キーワードをスペースで区切らないタイプ
        """
        if "search" in request.GET:
            medicines   = Medicine.objects.filter(name__contains=request.GET["search"])
        else:
            medicines   = Medicine.objects.all()
        """
        if "search" in request.GET:

            #(1)キーワードが空欄もしくはスペースのみの場合、ページにリダイレクト
            if request.GET["search"] == "" or request.GET["search"].isspace():
                return redirect("medicine:index")

            #(2)キーワードをリスト化させる(複数指定の場合に対応させるため)
            search      = request.GET["search"].replace("　"," ")
            search_list = search.split(" ")

            #(3)クエリを作る
            query       = Q()
            for word in search_list:
                #TIPS:AND検索の場合は&を、OR検索の場合は|を使用する。
                query |= Q(name__contains=word)

            #(4)作ったクエリを実行
            medicines   = Medicine.objects.filter(query)
        else:
            medicines   = Medicine.objects.all()

        context = { "medicines":medicines }

        return render(request,"medicine/index.html",context)

index   = IndexView.as_view()
