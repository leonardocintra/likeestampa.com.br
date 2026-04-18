# Dimona API V2 / V3

> Print-on-demand de camisetas e acessórios. Impressão local no Brasil (Rio de Janeiro) e EUA (Florida, Illinois).  
> **Base URL:** `https://admin.camisadimona.com.br`  
> **Conta:** Criar em [camisadimona.com.br](https://camisadimona.com.br)

---

## Autenticação

Todas as requisições exigem os seguintes headers:

```
api-key: SUA_API_KEY
Accept: application/json
Content-Type: application/json
```

**Rate Limiting:** 60 requisições por janela (headers `X-RateLimit-Limit` e `X-RateLimit-Remaining`).

---

## Índice de Rotas

| Método | Rota | Descrição |
|--------|------|-----------|
| `POST` | `/api/v2/order` | Criar pedido (designs como array) |
| `POST` | `/api/v3/order` | Criar pedido (designs nomeados por posição) |
| `GET` | `/api/v2/orders` | Listar todos os pedidos |
| `GET` | `/api/v2/order/{order-id}` | Buscar um pedido |
| `GET` | `/api/v2/order/{order-id}/tracking` | Histórico de rastreamento |
| `GET` | `/api/v2/order/{order-id}/timeline` | Timeline completa do pedido |
| `GET` | `/api/v2/order/{order-id}/items` | Itens do pedido |
| `POST` | `/api/v2/order/{order-id}/nfe` | Adicionar NFE ao pedido |
| `POST` | `/api/v2/order/{order-id}/shippingLabel` | Adicionar etiqueta de envio |
| `POST` | `/api/v2/order/{order-id}/shippingDocuments` | Adicionar NFE + etiqueta |
| `GET` | `/api/v2/sku/{sku_reference}/availability` | Verificar disponibilidade de SKU |
| `POST` | `/api/v2/shipping` | Cotar frete |

---

## 1. Criar Pedido (V2)

`POST /api/v2/order`

Cria um pedido de impressão. O campo `designs` é um **array ordenado** (frente, costas).

### Campos do Body

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `shipping_speed` | string | Sim* | `"pac"` ou `"sedex"`. Ignorado se `delivery_method_id` for enviado |
| `delivery_method_id` | string | Não | ID do método obtido via cotação de frete. Se presente, `shipping_speed` é ignorado |
| `order_id` | string | Sim | ID único do pedido (seu sistema). Deve ser único — duplicatas retornam erro |
| `customer_name` | string | Sim | Nome do cliente |
| `customer_document` | string | Não | CPF/CNPJ do cliente |
| `customer_email` | string | Não | Email do cliente |
| `webhook_url` | string | Não | URL para receber notificações de status (override do webhook global) |
| `items` | array | Sim | Lista de itens (ver abaixo) |
| `nfe` | object | Não | Dados da nota fiscal (ver abaixo) |
| `address` | object | Sim | Endereço de entrega (ver abaixo) |

### Objeto `items[]`

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `name` | string | Não | Nome descritivo do item |
| `sku` | string | Sim | SKU no seu sistema |
| `qty` | number | Sim | Quantidade |
| `dimona_sku_id` | string | Sim | SKU da Dimona (identifica produto + cor + tamanho) |
| `designs` | string[] | Sim | URLs das artes: `[url_frente, url_costas]` |
| `mocks` | string[] | Não | URLs dos mockups: `[mock_frente, mock_costas]` |

### Objeto `nfe`

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `chave` | string | Chave da NFe (44 dígitos) |
| `serie` | string | Série da nota |
| `numero` | string | Número da nota |
| `link` | string | URL para o PDF da DANFE |

### Objeto `address`

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `name` | string | Não | Nome do destinatário |
| `street` | string | Sim | Logradouro |
| `number` | string | Sim | Número |
| `complement` | string | Não | Complemento |
| `city` | string | Sim | Cidade |
| `state` | string | Sim | UF (2 letras) |
| `zipcode` | string | Sim | CEP (8 dígitos, sem traço) |
| `neighborhood` | string | Sim | Bairro |
| `phone` | string | Não | Telefone |
| `country` | string | Não | País (`"BR"` padrão) |

### Exemplo Request

```json
{
  "shipping_speed": "pac",
  "delivery_method_id": "177",
  "order_id": "pedido-12345",
  "customer_name": "Fulano da Silva",
  "customer_document": "123.456.789-13",
  "customer_email": "exemplo@gmail.com",
  "webhook_url": "https://meu-backend.com/webhooks/dimona",
  "items": [
    {
      "name": "Camisa Polo P Branca",
      "sku": "12345",
      "qty": 2,
      "dimona_sku_id": "010603110108",
      "designs": [
        "https://storage.exemplo.com/arte-frente.png",
        "https://storage.exemplo.com/arte-costas.png"
      ],
      "mocks": [
        "https://storage.exemplo.com/mock-frente.png",
        "https://storage.exemplo.com/mock-costas.png"
      ]
    },
    {
      "name": "Camisa Polo M Branca",
      "sku": "12346",
      "qty": 2,
      "dimona_sku_id": "010603110109",
      "designs": [
        "https://storage.exemplo.com/arte-frente.png",
        "https://storage.exemplo.com/arte-costas.png"
      ],
      "mocks": [
        "https://storage.exemplo.com/mock-frente.png",
        "https://storage.exemplo.com/mock-costas.png"
      ]
    }
  ],
  "nfe": {
    "chave": "33180513570097000110550010000166321270551123",
    "serie": "1",
    "numero": "1234",
    "link": "https://link-para-pdf-danfe.com.br"
  },
  "address": {
    "name": "Receiver Name",
    "street": "Rua Buenos Aires",
    "number": "334",
    "complement": "Loja",
    "city": "Rio de Janeiro",
    "state": "RJ",
    "zipcode": "20061000",
    "neighborhood": "Centro",
    "phone": "21 21093661",
    "country": "BR"
  }
}
```

### Response — `200 OK`

```json
{
  "order": "064-435-556"
}
```

O campo `order` é o **dimona_id** — usar para consultas futuras.

### Response — `422 Unprocessable Entity`

```json
"O pedido pedido-12345 já existe"
```

---

## 2. Criar Pedido (V3) — Designs Nomeados

`POST /api/v3/order`

Idêntico ao V2, mas o campo `designs` e `mocks` são **objetos com posições nomeadas** em vez de arrays.

### Diferença no `items[]`

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `designs` | object | Objeto com posições: `front`, `back`, `left_sleeve`, `right_sleeve`, `inner_label`, `outer_label` |
| `mocks` | object | Mesmo formato que `designs`, com URLs dos mockups |

### Exemplo de Item (V3)

```json
{
  "name": "Camisa Polo M Branca",
  "sku": "12346",
  "qty": 2,
  "dimona_sku_id": "010603110109",
  "designs": {
    "front": "https://storage.exemplo.com/arte-frente.png",
    "back": "https://storage.exemplo.com/arte-costas.png",
    "left_sleeve": "https://storage.exemplo.com/arte-manga-esq.png",
    "right_sleeve": "https://storage.exemplo.com/arte-manga-dir.png",
    "inner_label": "https://storage.exemplo.com/etiqueta-interna.png",
    "outer_label": "https://storage.exemplo.com/etiqueta-externa.png"
  },
  "mocks": {
    "front": "https://storage.exemplo.com/mock-frente.png",
    "back": "https://storage.exemplo.com/mock-costas.png",
    "left_sleeve": "https://storage.exemplo.com/mock-manga-esq.png",
    "right_sleeve": "https://storage.exemplo.com/mock-manga-dir.png",
    "inner_label": "https://storage.exemplo.com/mock-etiqueta-interna.png",
    "outer_label": "https://storage.exemplo.com/mock-etiqueta-externa.png"
  }
}
```

### Posições Disponíveis

| Chave | Posição |
|-------|---------|
| `front` | Frente |
| `back` | Costas |
| `left_sleeve` | Manga esquerda |
| `right_sleeve` | Manga direita |
| `inner_label` | Etiqueta interna |
| `outer_label` | Etiqueta externa |

### Responses

Iguais ao V2 (`200` com `{ "order": "xxx-xxx-xxx" }` ou `422`).

---

## 3. Listar Pedidos

`GET /api/v2/orders`

Retorna a lista de todos os pedidos da conta.

---

## 4. Buscar Pedido

`GET /api/v2/order/{order-id}`

Retorna os detalhes de um pedido específico. Usar o `dimona_id` retornado na criação.

### Response — `200 OK`

```json
{
  "dimona_id": "123-123-123",
  "seller_id": "abcd",
  "status": "Aguardando Imagens",
  "shipping_cost": 17.99,
  "shipping_method_name": "Correios Sedex",
  "total_value": 67.99,
  "status_id": 18,
  "created_at": "01/01/2000",
  "tracking_url": "http://status.ondeestameupedido.com/tracking/1168/123123123",
  "tracking_code": null
}
```

### Campos da Response

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `dimona_id` | string | ID do pedido na Dimona |
| `seller_id` | string | ID do vendedor |
| `status` | string | Status textual do pedido |
| `status_id` | number | ID numérico do status |
| `shipping_cost` | number | Custo do frete (R$) |
| `shipping_method_name` | string | Método de envio |
| `total_value` | number | Valor total (R$) |
| `created_at` | string | Data de criação |
| `tracking_url` | string | URL de rastreamento público |
| `tracking_code` | string \| null | Código de rastreio da transportadora |

---

## 5. Rastreamento do Pedido

`GET /api/v2/order/{order-id}/tracking`

Retorna o histórico de rastreamento logístico (eventos da transportadora).

### Response — `200 OK`

```json
[
  {
    "status_name": "Entregue",
    "micro_status_name": "ENTREGUE NO LOCAL DE RETIRADA",
    "micro_status_description": "A carga está em processo de transferência entre filiais.",
    "message": "FL RIO DE JANEIRO",
    "event_date": {
      "date": "2018-08-08 17:54:00.000000",
      "timezone_type": 3,
      "timezone": "America/Sao_Paulo"
    },
    "created_at": "2018-08-09 14:33:57"
  }
]
```

### Campos de cada evento

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `status_name` | string | Status macro (Entregue, Em Trânsito, etc.) |
| `micro_status_name` | string | Substatus detalhado |
| `micro_status_description` | string | Descrição do micro status |
| `message` | string | Localização/mensagem do evento |
| `event_date` | object | Data/hora do evento (timezone `America/Sao_Paulo`) |
| `created_at` | string | Quando o evento foi registrado no sistema |

---

## 6. Timeline do Pedido

`GET /api/v2/order/{order-id}/timeline`

Retorna a timeline completa do pedido, incluindo **todos** os tipos de evento:

- **Alteração de status** — Em produção, enviado, entregue, cancelado, etc.
- **Produção** — Status de cada etiqueta (item): criada, pickada, embalada, QC, cancelada
- **Ações automáticas** — NFe criada, etiqueta de envio gerada
- **Transações** — Pagamento aprovado, boleto emitido
- **Rastreamento** — Atualizações da transportadora

### Response — `200 OK`

```json
[
  {
    "icon": "glyphicon-check",
    "title": "Alteração de Status",
    "text": "Status alterado de Pagamento Aprovado para Cancelado",
    "color": "warning",
    "timestamp": "17/09/19 13:50:32"
  },
  {
    "icon": "glyphicon-circle-arrow-right",
    "title": "Produção",
    "text": "Status da etiqueta 123456 alterado de Etiqueta Criada para Cancelada",
    "color": "danger",
    "timestamp": "17/09/19 13:50:32"
  },
  {
    "icon": "glyphicon-circle-arrow-right",
    "title": "Produção",
    "text": "Etiqueta 123456 criada.",
    "color": "danger",
    "timestamp": "17/09/19 13:49:56"
  },
  {
    "icon": "glyphicon-check",
    "title": "Alteração de Status",
    "text": "Status alterado de Pagamento Pendente para Pagamento Aprovado",
    "color": "warning",
    "timestamp": "17/09/19 13:49:55"
  }
]
```

### Campos de cada evento

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `icon` | string | Classe do ícone (glyphicon) |
| `title` | string | Tipo do evento |
| `text` | string | Descrição detalhada |
| `color` | string | `"warning"`, `"danger"`, `"success"`, `"info"` |
| `timestamp` | string | Data/hora (formato `DD/MM/YY HH:mm:ss`) |

---

## 7. Itens do Pedido

`GET /api/v2/order/{order-id}/items`

Retorna os itens de um pedido com status individual de produção por etiqueta.

---

## 8. Adicionar NFE ao Pedido

`POST /api/v2/order/{order-id}/nfe`

> **Atenção:** Antes de usar este endpoint, envie um email para `api@dimona.com.br`.

### Request Body

```json
{
  "chave": "33180513570097000110550010000166321270551123",
  "serie": "1",
  "numero": "1234",
  "link": "https://link-para-pdf-danfe.com.br"
}
```

---

## 9. Adicionar Etiqueta de Envio

`POST /api/v2/order/{order-id}/shippingLabel`

> **Atenção:** Antes de usar este endpoint, envie um email para `api@dimona.com.br`.

### Request Body

```json
{
  "link": "https://link-para-etiqueta.com.br"
}
```

---

## 10. Adicionar NFE + Etiqueta

`POST /api/v2/order/{order-id}/shippingDocuments`

> **Atenção:** Antes de usar este endpoint, envie um email para `api@dimona.com.br`.

Envia NFE e etiqueta de envio em uma única request.

### Request Body

```json
{
  "nfe": "https://storage.exemplo.com/nfe/pedido-123_Invoice.pdf",
  "label": "https://storage.exemplo.com/labels/pedido-123_Shipping.pdf"
}
```

---

## 11. Verificar Disponibilidade de SKU

`GET /api/v2/sku/{sku_reference}/availability`

Verifica a disponibilidade de estoque de um produto por referência do SKU.

### Response

Retorna um objeto onde as chaves são IDs de cor e os valores são objetos com IDs de tamanho mapeados para quantidades disponíveis:

```json
{
  "idCor1": {
    "idTamanho1": 150,
    "idTamanho2": 200
  },
  "idCor2": {
    "idTamanho1": 0,
    "idTamanho2": 75
  }
}
```

---

## 12. Cotar Frete

`POST /api/v2/shipping`

Calcula opções de frete com base no CEP e quantidade de itens.

### Request Body

```json
{
  "zipcode": "20061001",
  "quantity": "1"
}
```

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `zipcode` | string | CEP de destino (8 dígitos) |
| `quantity` | string | Quantidade total de itens |

### Response — `200 OK`

```json
[
  {
    "name": "Correios Sedex",
    "value": 10.34,
    "business_days": 6,
    "delivery_method_id": 2
  },
  {
    "name": "Jadlog Econômica",
    "value": 15.35,
    "business_days": 10,
    "delivery_method_id": 177
  },
  {
    "name": "Jadlog Express",
    "value": 15.57,
    "business_days": 9,
    "delivery_method_id": 176
  },
  {
    "name": "Buslog",
    "value": 24.32,
    "business_days": 5,
    "delivery_method_id": 780
  }
]
```

### Campos de cada opção

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `name` | string | Nome da transportadora + serviço |
| `value` | number | Custo do frete em R$ |
| `business_days` | number | Prazo de entrega em dias úteis |
| `delivery_method_id` | number | ID para usar no campo `delivery_method_id` ao criar pedido |

> **Dica:** Use o `delivery_method_id` retornado aqui no campo `delivery_method_id` do `POST /api/v2/order` para selecionar o frete exato. Quando esse campo é enviado, o `shipping_speed` é ignorado.

---

## 13. Webhook — Notificações de Status

Configure a URL de webhook em: `www.camisadimona.com.br/loja/conta/avancado`

Ou envie `webhook_url` por pedido na criação.

A Dimona envia um `POST` para sua URL a cada mudança de status:

### Payload recebido

```json
{
  "api_key": "YOUR_API_KEY",
  "dimona_id": "462-424-866",
  "status_id": 13,
  "name": "Faturado",
  "seller_id": "1524594756",
  "tracking_url": "http://status.ondeestameupedido.com/tracking/1168/462424866"
}
```

### Campos

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `api_key` | string | Sua API key (para validação) |
| `dimona_id` | string | ID do pedido na Dimona |
| `status_id` | number | ID numérico do novo status |
| `name` | string | Nome do status em texto |
| `seller_id` | string | ID do pedido no seu sistema (o `order_id` que você enviou) |
| `tracking_url` | string | URL pública de rastreamento |
