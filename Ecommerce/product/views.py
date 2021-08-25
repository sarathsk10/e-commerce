from _datetime import datetime
import requests
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.decorators import api_view
from product.models import Product
from product.serializer import productserializer
from rest_framework.views import APIView


@api_view(['GET'])
def productviewapi(request):
        if request.method=='GET':
            results=Product.objects.all()
            ser=productserializer(results,many=True)
            return Response(ser.data)
def productview(request):
    if request.method=="GET":
        callapi = requests.get('http://127.0.0.1:8000/productviewapi')
        results = callapi.json()
        return render(request,'ProductView.html',{'Product':results})


def serialiazeobj(args):
    pass


# class Product_upd_del(APIView):
#     def get_object(self,pk):
#         try:
#             return Product.objects.get(pk=pk)
#         except Product.DoesNotExist:
#             return Response(serialiazeobj.errors,status=status.HTTP_400_BAD_REQUEST)
#     def get(self,request,pk):
#         probj=self.get_object(pk)
#         serialiazeobj=productserializer(probj)
#         return Response(serialiazeobj.data)
#     def put(self,request):
#         probj=self.get_object()
#         proserialize=productserializer(probj,data=request.data)
#         if proserialize.is_valid():
#             proserialize.save()
#             return Response(proserialize.data,status=status.HTTP_200_OK)
#         return Response(proserialize.errors,status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self,request,pk):
#         probj = self.get_object(pk)
#         probj.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def productaddviewapi(request):
        if request.method=='POST':
            ser=productserializer(data=request.data)
            if ser.is_valid():
                ser.save()
                return Response(ser.data, status=status.HTTP_201_CREATED)
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

def productaddview(request):
    if request.method=="POST":
        p_name=request.POST.get('pname')
        c_id=str(request.session['logid'])
        price=request.POST.get('price')
        # regdt=request.POST.get('regd')
        regdt=datetime.now()
        regdt1=regdt.strftime("%Y-%m-%d")
        status='Pending'
        data={'p_name':p_name,'c_id':c_id,'price':price,'regdt':regdt1,'status':status}
        headers={'Content-Type': 'application/json'}
        read=requests.post('http://127.0.0.1:8000/productaddviewapi', json=data, headers=headers)
        return render(request,'productAdd.html')
    else:
        return render(request,'productAdd.html')

@api_view(['DELETE'])
def delete(request,pk):
    probj = Product.objects.get(pk=pk)
    probj.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

def deletev(requset,idd):
    return delete(requset,idd)

def active(request):
        tp=str(request.session['ex'])
        obj=Product.objects.get(p_id=tp)
        obj.status = "Active"
        if obj.c_id==str(request.session['logid']):
            obj.save()
            return productview(request)
        else:
            return HttpResponse('<h2>Invalid option... please select with your customer_id</h2>')

def act(requset,idd):
    requset.session['ex'] = idd
    return active(requset)

def inactive(request):
        tp = str(request.session['ex'])
        obj = Product.objects.get(p_id=tp)
        datein=obj.regdt
        regdt1 = datetime.now()
        if (regdt1.date()-datein).days >56:
            obj.status = "Inctive"
            if obj.c_id==str(request.session['logid']):
                obj.save()
                return productview(request)
            else:
                return HttpResponse('<h2>Invalid option... please select with your customer_id</h2>')
        return productview(request)

def inact(requset, idd):
    requset.session['ex'] = idd

    return inactive(requset)

