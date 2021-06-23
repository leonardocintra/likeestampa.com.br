

from checkout.forms import ClienteForm
from services.peoplesoft.peoplesoft import buscar_cliente_by_id


def get_cliente_data_form(request):
    form = ClienteForm()

    if 'cliente_id' in request.session:
        cliente = buscar_cliente_by_id(request.session['cliente_id'])
        cliente = cliente['records'][0]
        endereco = cliente['enderecos'][0]
        form.fields['cpf'].initial = cliente['cpf']
        form.fields['nome'].initial = cliente['nome']
        form.fields['email'].initial = cliente['email']
        form.fields['cep'].initial = endereco['cep']
        form.fields['cidade'].initial = endereco['cidade']
        form.fields['uf'].initial = endereco['uf']
        form.fields['numero'].initial = endereco['numero']
        form.fields['bairro'].initial = endereco['bairro']
        form.fields['endereco'].initial = endereco['endereco']
        form.fields['complemento'].initial = endereco['complemento']
        form.fields['referencia'].initial = endereco['referencia']

        form.fields['cpf'].widget.attrs['readonly'] = True
        form.fields['nome'].widget.attrs['readonly'] = True
        form.fields['email'].widget.attrs['readonly'] = True
        form.fields['cep'].widget.attrs['readonly'] = True
        form.fields['cidade'].widget.attrs['readonly'] = True
        form.fields['uf'].widget.attrs['readonly'] = True
        form.fields['numero'].widget.attrs['readonly'] = True
        form.fields['bairro'].widget.attrs['readonly'] = True
        form.fields['endereco'].widget.attrs['readonly'] = True
        form.fields['complemento'].widget.attrs['readonly'] = True
        form.fields['referencia'].widget.attrs['readonly'] = True

    return form
