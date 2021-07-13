

from checkout.forms import ClienteForm
from services.peoplesoft.peoplesoft import buscar_cliente_by_id


def get_cliente_data_form(request):
    form = ClienteForm()

    if 'cliente_id' in request.session:
        cliente = buscar_cliente_by_id(request.session['cliente_id'])
        cliente = cliente['records'][0]
        enderecos = cliente['enderecos'][0]
        
        if cliente['telefones']:
            telefones = cliente['telefones'][0]
            form.fields['area'].initial = telefones['area']
            form.fields['telefone_numero'].initial = telefones['numero']
            form.fields['tipo'].initial = telefones['tipo']
        form.fields['cep'].initial = enderecos['cep']
        form.fields['cpf'].initial = cliente['cpf']
        form.fields['nome'].initial = cliente['nome']
        form.fields['email'].initial = cliente['email']
        form.fields['cidade'].initial = enderecos['cidade']
        form.fields['uf'].initial = enderecos['uf']
        form.fields['numero'].initial = enderecos['numero']
        form.fields['bairro'].initial = enderecos['bairro']
        form.fields['endereco'].initial = enderecos['endereco']
        form.fields['complemento'].initial = enderecos['complemento']
        form.fields['referencia'].initial = enderecos['referencia']

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
