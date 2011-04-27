# http://docs.djangoproject.com/en/1.3/howto/custom-template-tags/#passing-template-variables-to-the-tag

from django import template

register = template.Library()

def metaform(item, meta):
    t = meta.form_type
    try:
        val = getattr(item, meta.slug)
    except:
        val = ''
    if t == 'file':
        return '<input type="file" name="'+meta.slug+'" id="'+meta.slug+'" value=""/>'
    elif t == 'select':
        v = '<select name="'+meta.slug+'">'
        for opt in re.split("\n", meta.attribute):
            v += '<option value="'+opt+'">'+opt+'</option>'
        v += '</select>'
        return v
    elif t == 'textarea':
        return '<textarea name="'+meta.slug+'" style="width:100%;">'+val+'</textarea>'
    return '<input type="text" name="'+meta.slug+'" id="'+meta.slug+'" value="'+val+'" style="width:90%" />'
metaform.is_safe = True
register.filter('metaform', metaform)
 
def metaview(item, meta):
    if meta.form_type == 'file':
        return ''
    try:
        return getattr(item, meta.slug)
    except:
        return ''
metaview.is_safe = True
register.filter('metaview', metaview)
