from django import template
register = template.Library()

@register.simple_tag()
def sirarti(context):
    sira=context+1
    return sira


@register.filter(name='kalan_zaman')
def kalan_zaman(val,val2):
    return val-val2

@register.filter(name='carp')
def carp(val,val2):
    return val*val2


@register.filter(name='topla')
def topla(val1,val2):
    return val1+val2