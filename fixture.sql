INSERT INTO subcategoria (id, nome, slug, created_at, updated_at, icone_fontawesome, ativo) VALUES(2, 'Banda / Cantores', 'banda-cantores', '2021-04-20 21:00:00.000', '2021-04-20 21:00:00.000', 'microphone-alt', false);
INSERT INTO subcategoria (id, nome, slug, created_at, updated_at, icone_fontawesome, ativo) VALUES(5, 'Religião', 'religiao', '2021-04-20 21:00:00.000', '2021-04-20 21:00:00.000', 'church', false);
INSERT INTO subcategoria (id, nome, slug, created_at, updated_at, icone_fontawesome, ativo) VALUES(6, 'Bebidas / Comidas', 'bebidas-comidas', '2021-04-20 21:00:00.000', '2021-04-20 21:00:00.000', 'hamburger', false);
INSERT INTO subcategoria (id, nome, slug, created_at, updated_at, icone_fontawesome, ativo) VALUES(7, 'Automoveis', 'automoveis', '2021-04-21 21:00:00.000', '2021-04-21 21:00:00.000', 'car', false);
INSERT INTO subcategoria (id, nome, slug, created_at, updated_at, icone_fontawesome, ativo) VALUES(8, 'Universo / Espaço', 'universo-espaco', '2021-04-21 21:00:00.000', '2021-04-21 21:00:00.000', 'rocket', false);
INSERT INTO subcategoria (id, nome, slug, created_at, updated_at, icone_fontawesome, ativo) VALUES(9, 'Redes Sociais', 'redes-sociais', '2021-04-21 21:00:00.000', '2021-04-21 21:00:00.000', 'laptop', false);
INSERT INTO subcategoria (id, nome, slug, created_at, updated_at, icone_fontawesome, ativo) VALUES(11, 'Frases', 'frases', '2021-05-20 21:00:00.000', '2021-05-20 21:00:00.000', 'quote-right', true);
INSERT INTO subcategoria (id, nome, slug, created_at, updated_at, icone_fontawesome, ativo) VALUES(3, 'Filmes', 'filmes', '2021-04-20 21:00:00.000', '2021-05-20 21:00:00.000', 'video', true);
INSERT INTO subcategoria (id, nome, slug, created_at, updated_at, icone_fontawesome, ativo) VALUES(10, 'Vídeo Game', 'video-game', '2021-04-22 21:00:00.000', '2021-05-20 21:00:00.000', 'gamepad', true);
INSERT INTO subcategoria (id, nome, slug, created_at, updated_at, icone_fontawesome, ativo) VALUES(12, 'Rostos', 'rostos', '2021-05-20 21:00:00.000', '2021-05-20 21:00:00.000', 'smile', true);
INSERT INTO subcategoria (id, nome, slug, created_at, updated_at, icone_fontawesome, ativo) VALUES(4, 'Times de Futebol', 'times-de-futebol', '2021-04-20 21:00:00.000', '2021-05-26 21:00:00.000', 'futbol', true);
INSERT INTO subcategoria (id, nome, slug, created_at, updated_at, icone_fontawesome, ativo) VALUES(1, 'Programação', 'programacao', '2021-04-20 21:00:00.000', '2021-05-26 21:00:00.000', 'laptop-code', true);
INSERT INTO subcategoria (id, nome, slug, created_at, updated_at, icone_fontawesome, ativo) VALUES(13, 'Profissões', 'profissoes', '2021-07-19 13:32:42.338', '2021-07-19 13:32:42.338', 'briefcase', true);
INSERT INTO seller (id, nome, site, cep, endereco, numero, bairro, complemento, referencia, cidade, uf, observacao, created_at, updated_at, nome_contato, telefone_contato, frete_tipo, frete_token, frete_url, ativo) VALUES(1, 'Dimona', 'https://camisadimona.com.br/loja/conta/pedidos', '13898989', 'Rua 6 de Abril', '1302', 'Centro', NULL, NULL, 'Franca', 'MG', '', '2021-07-19 13:32:07.842', '2021-07-19 13:32:07.842', 'Nenhum', '392839823989', 'proprio', '', NULL, true);

INSERT INTO produto (id, nome, descricao, slug, created_at, updated_at, subcategoria_id, ativo, imagem_principal, preco_base, genero, seller_id, imagem_design) VALUES(1, 'Python', 'Camiseta Linguagem de programação Python

Malha cardada fio 24.1
100% algodão
Modelagem com caimento reto
Acabamento com costura simples, gola em ribana

Percentual de encolhimento pós lavagem: 3,70%', 'python', '2021-04-20 21:00:00.000', '2021-06-26 21:00:00.000', 1, true, 'image/upload/v1621297115/hkjlfsghx1wyz2bf3xk8.png', 35.00, 'M', 1, 'NAO_INFORMADO');
INSERT INTO produto (id, nome, descricao, slug, created_at, updated_at, subcategoria_id, ativo, imagem_principal, preco_base, genero, seller_id, imagem_design) VALUES(5, 'Sao Paulo', 'Camiseta do Tricolor Paulista

Malha cardada fio 24.1
100% algodão
Modelagem com caimento reto
Acabamento com costura simples, gola em ribana

Percentual de encolhimento pós lavagem: 3,70%', 'sao-paulo', '2021-04-20 21:00:00.000', '2021-06-26 21:00:00.000', 4, true, 'image/upload/v1621297101/ngikdcvoqdevogoctgey.png', 35.00, 'M', 1, 'NAO_INFORMADO');
INSERT INTO produto (id, nome, descricao, slug, created_at, updated_at, subcategoria_id, ativo, imagem_principal, preco_base, genero, seller_id, imagem_design) VALUES(19, 'Basic Style', 'Basic Style

Malha cardada fio 24.1
100% algodão
Modelagem com caimento reto
Acabamento com costura simples, gola em ribana

Percentual de encolhimento pós lavagem: 3,70%', 'basic-style', '2021-05-20 21:00:00.000', '2021-06-26 21:00:00.000', 12, true, 'image/upload/v1621641495/bj5idlflrjlqj92cfdwt.png', 35.00, 'F', 1, 'NAO_INFORMADO');
INSERT INTO produto (id, nome, descricao, slug, created_at, updated_at, subcategoria_id, ativo, imagem_principal, preco_base, genero, seller_id, imagem_design) VALUES(20, 'Django', 'Camiseta Framework Django

Malha cardada fio 24.1
100% algodão
Modelagem com caimento reto
Acabamento com costura simples, gola em ribana

Percentual de encolhimento pós lavagem: 3,70%', 'django', '2021-05-24 21:00:00.000', '2021-06-26 21:00:00.000', 1, true, 'image/upload/v1621945952/nprlzb1zmc8wl7y7ka5g.png', 35.00, 'M', 1, 'NAO_INFORMADO');
INSERT INTO produto (id, nome, descricao, slug, created_at, updated_at, subcategoria_id, ativo, imagem_principal, preco_base, genero, seller_id, imagem_design) VALUES(18, 'Love', 'Love

Malha cardada fio 24.1
100% algodão
Modelagem com caimento reto
Acabamento com costura simples, gola em ribana

Percentual de encolhimento pós lavagem: 3,70%', 'love-only', '2021-05-20 21:00:00.000', '2021-06-26 21:00:00.000', 11, true, 'image/upload/v1621641389/wkh4xrhzk6c4qh2qavlq.png', 35.00, 'F', 1, 'NAO_INFORMADO');
INSERT INTO produto (id, nome, descricao, slug, created_at, updated_at, subcategoria_id, ativo, imagem_principal, preco_base, genero, seller_id, imagem_design) VALUES(17, 'Love Oncinha', 'Love Oncinha

Malha cardada fio 24.1
100% algodão
Modelagem com caimento reto
Acabamento com costura simples, gola em ribana

Percentual de encolhimento pós lavagem: 3,70%', 'love-oncinha', '2021-05-20 21:00:00.000', '2021-06-26 21:00:00.000', 11, true, 'image/upload/v1621641216/ovftnmxzm1alanppw2vg.png', 35.00, 'F', 1, 'NAO_INFORMADO');
INSERT INTO produto (id, nome, descricao, slug, created_at, updated_at, subcategoria_id, ativo, imagem_principal, preco_base, genero, seller_id, imagem_design) VALUES(21, 'NodeJS', 'Camiseta NodeJS

Malha cardada fio 24.1
100% algodão
Modelagem com caimento reto
Acabamento com costura simples, gola em ribana

Percentual de encolhimento pós lavagem: 3,70%', 'camiseta-nodejs', '2021-05-24 21:00:00.000', '2021-06-26 21:00:00.000', 1, true, 'image/upload/v1621945974/ywfdassk9yetnloakkgp.png', 35.00, 'M', 1, 'NAO_INFORMADO');
INSERT INTO produto (id, nome, descricao, slug, created_at, updated_at, subcategoria_id, ativo, imagem_principal, preco_base, genero, seller_id, imagem_design) VALUES(22, 'Curso Direito', 'Teste', 'curso-direito', '2021-07-19 13:34:22.356', '2021-07-19 13:35:44.176', 13, true, 'image/upload/v1626712460/pzgsztmvyahrbhgohhmk.jpg', 51.90, 'F', 1, 'image/upload/v1626712461/scqayro9kqztqbw7uc5u.png');
INSERT INTO produto (id, nome, descricao, slug, created_at, updated_at, subcategoria_id, ativo, imagem_principal, preco_base, genero, seller_id, imagem_design) VALUES(23, 'Camiseta Odonto', 'Odeonto paiuafsdfasfdashdfa]s
dfasdfasdfasdhfakdfhasldhfaçsdf asdf asd
fasdfasdjfahsdfjas
dfa
sfa
sf
asf
asdfasdfsfdsf', 'camiseta-odonto', '2021-08-04 23:22:56.971', '2021-08-04 23:22:56.971', 13, true, 'image/upload/v1628130175/zvdvtygbqfwudnfbbqik.png', 51.90, 'F', 1, 'image/upload/v1628130176/o7m2hca7jmwkqimepgxb.png');
INSERT INTO variacao (id, descricao, ativo, created_at, updated_at) VALUES(3, 'Cor', true, '2021-06-06 21:00:00.000', '2021-06-07 21:00:00.000');
INSERT INTO variacao (id, descricao, ativo, created_at, updated_at) VALUES(4, 'Tamanho', true, '2021-06-06 21:00:00.000', '2021-06-07 21:00:00.000');
INSERT INTO tipo_variacao (id, descricao, ativo, created_at, updated_at, variacao_id, preco_variacao, valor_adicional) VALUES(3, 'P', true, '2021-06-07 21:00:00.000', '2021-06-07 21:00:00.000', 4, 51.90, NULL);
INSERT INTO tipo_variacao (id, descricao, ativo, created_at, updated_at, variacao_id, preco_variacao, valor_adicional) VALUES(4, 'M', true, '2021-06-07 21:00:00.000', '2021-06-07 21:00:00.000', 4, 51.90, NULL);
INSERT INTO tipo_variacao (id, descricao, ativo, created_at, updated_at, variacao_id, preco_variacao, valor_adicional) VALUES(5, 'G', true, '2021-06-07 21:00:00.000', '2021-06-07 21:00:00.000', 4, 51.90, NULL);
INSERT INTO tipo_variacao (id, descricao, ativo, created_at, updated_at, variacao_id, preco_variacao, valor_adicional) VALUES(6, 'GG', true, '2021-06-07 21:00:00.000', '2021-06-07 21:00:00.000', 4, 51.90, NULL);
INSERT INTO tipo_variacao (id, descricao, ativo, created_at, updated_at, variacao_id, preco_variacao, valor_adicional) VALUES(1, '-- NAO INFORMADO --', true, '2021-06-07 21:00:00.000', '2021-06-26 21:00:00.000', 3, 51.90, NULL);
INSERT INTO tipo_variacao (id, descricao, ativo, created_at, updated_at, variacao_id, preco_variacao, valor_adicional) VALUES(8, 'Branco', true, '2021-06-26 21:00:00.000', '2021-06-26 21:00:00.000', 3, 51.90, NULL);
INSERT INTO tipo_variacao (id, descricao, ativo, created_at, updated_at, variacao_id, preco_variacao, valor_adicional) VALUES(7, 'Azul Royal', true, '2021-06-15 21:00:00.000', '2021-08-04 23:20:16.598', 3, 51.90, '#004BAA');
INSERT INTO tipo_variacao (id, descricao, ativo, created_at, updated_at, variacao_id, preco_variacao, valor_adicional) VALUES(2, 'Vermelho', true, '2021-06-07 21:00:00.000', '2021-08-04 23:21:03.187', 3, 51.90, '#FF1726');
INSERT INTO tipo_variacao (id, descricao, ativo, created_at, updated_at, variacao_id, preco_variacao, valor_adicional) VALUES(9, 'Cinza Mescla', true, '2021-08-04 23:22:48.886', '2021-08-04 23:22:48.886', 3, 51.90, '#BEC0C3');
INSERT INTO modelo (id, descricao, created_at, updated_at, descricao_cliente) VALUES(1, 'T-Shirt', '2021-07-23 19:56:47.798', '2021-08-04 23:18:07.099', 'T-Shirt');
INSERT INTO modelo (id, descricao, created_at, updated_at, descricao_cliente) VALUES(2, 'Baby Long', '2021-08-04 23:18:20.175', '2021-08-04 23:18:20.175', 'T-Shirt Feminina');
INSERT INTO modelo_variacao (id, created_at, updated_at, tipo_variacao_id, imagem, modelo_produto_id, outras_informacoes) VALUES(7, '2021-06-15 21:00:00.000', '2021-06-15 21:00:00.000', 3, NULL, NULL, NULL);
INSERT INTO modelo_variacao (id, created_at, updated_at, tipo_variacao_id, imagem, modelo_produto_id, outras_informacoes) VALUES(8, '2021-06-15 21:00:00.000', '2021-06-15 21:00:00.000', 4, NULL, NULL, NULL);
INSERT INTO modelo_variacao (id, created_at, updated_at, tipo_variacao_id, imagem, modelo_produto_id, outras_informacoes) VALUES(9, '2021-06-15 21:00:00.000', '2021-06-15 21:00:00.000', 5, NULL, NULL, NULL);
INSERT INTO modelo_variacao (id, created_at, updated_at, tipo_variacao_id, imagem, modelo_produto_id, outras_informacoes) VALUES(10, '2021-06-15 21:00:00.000', '2021-06-15 21:00:00.000', 6, NULL, NULL, NULL);
INSERT INTO modelo_variacao (id, created_at, updated_at, tipo_variacao_id, imagem, modelo_produto_id, outras_informacoes) VALUES(6, '2021-06-15 21:00:00.000', '2021-06-15 21:00:00.000', 1, NULL, NULL, NULL);
INSERT INTO modelo_variacao (id, created_at, updated_at, tipo_variacao_id, imagem, modelo_produto_id, outras_informacoes) VALUES(11, '2021-06-15 21:00:00.000', '2021-06-15 21:00:00.000', 3, NULL, NULL, NULL);
INSERT INTO modelo_variacao (id, created_at, updated_at, tipo_variacao_id, imagem, modelo_produto_id, outras_informacoes) VALUES(12, '2021-06-15 21:00:00.000', '2021-06-15 21:00:00.000', 4, NULL, NULL, NULL);
INSERT INTO modelo_variacao (id, created_at, updated_at, tipo_variacao_id, imagem, modelo_produto_id, outras_informacoes) VALUES(13, '2021-06-15 21:00:00.000', '2021-06-15 21:00:00.000', 5, NULL, NULL, NULL);
INSERT INTO modelo_variacao (id, created_at, updated_at, tipo_variacao_id, imagem, modelo_produto_id, outras_informacoes) VALUES(14, '2021-06-15 21:00:00.000', '2021-06-15 21:00:00.000', 6, NULL, NULL, NULL);
INSERT INTO modelo_variacao (id, created_at, updated_at, tipo_variacao_id, imagem, modelo_produto_id, outras_informacoes) VALUES(15, '2021-06-15 21:00:00.000', '2021-06-15 21:00:00.000', 1, NULL, NULL, NULL);
INSERT INTO modelo_variacao (id, created_at, updated_at, tipo_variacao_id, imagem, modelo_produto_id, outras_informacoes) VALUES(16, '2021-06-25 21:00:00.000', '2021-06-25 21:00:00.000', 3, NULL, 1, NULL);
INSERT INTO modelo_variacao (id, created_at, updated_at, tipo_variacao_id, imagem, modelo_produto_id, outras_informacoes) VALUES(17, '2021-06-25 21:00:00.000', '2021-06-25 21:00:00.000', 4, NULL, 1, NULL);
INSERT INTO modelo_variacao (id, created_at, updated_at, tipo_variacao_id, imagem, modelo_produto_id, outras_informacoes) VALUES(18, '2021-06-25 21:00:00.000', '2021-06-25 21:00:00.000', 5, NULL, 1, NULL);
INSERT INTO modelo_variacao (id, created_at, updated_at, tipo_variacao_id, imagem, modelo_produto_id, outras_informacoes) VALUES(19, '2021-06-25 21:00:00.000', '2021-06-25 21:00:00.000', 6, NULL, 1, NULL);
INSERT INTO modelo_variacao (id, created_at, updated_at, tipo_variacao_id, imagem, modelo_produto_id, outras_informacoes) VALUES(20, '2021-06-25 21:00:00.000', '2021-06-26 21:00:00.000', 8, NULL, 1, NULL);
INSERT INTO modelo_variacao (id, created_at, updated_at, tipo_variacao_id, imagem, modelo_produto_id, outras_informacoes) VALUES(21, '2021-06-26 21:00:00.000', '2021-06-26 21:00:00.000', 3, NULL, 2, NULL);
INSERT INTO modelo_variacao (id, created_at, updated_at, tipo_variacao_id, imagem, modelo_produto_id, outras_informacoes) VALUES(22, '2021-06-26 21:00:00.000', '2021-06-26 21:00:00.000', 4, NULL, 2, NULL);
INSERT INTO modelo_variacao (id, created_at, updated_at, tipo_variacao_id, imagem, modelo_produto_id, outras_informacoes) VALUES(23, '2021-06-26 21:00:00.000', '2021-06-26 21:00:00.000', 5, NULL, 2, NULL);
INSERT INTO modelo_variacao (id, created_at, updated_at, tipo_variacao_id, imagem, modelo_produto_id, outras_informacoes) VALUES(24, '2021-06-26 21:00:00.000', '2021-06-26 21:00:00.000', 6, NULL, 2, NULL);
INSERT INTO modelo_variacao (id, created_at, updated_at, tipo_variacao_id, imagem, modelo_produto_id, outras_informacoes) VALUES(25, '2021-06-26 21:00:00.000', '2021-06-26 21:00:00.000', 3, NULL, 3, NULL);
INSERT INTO modelo_variacao (id, created_at, updated_at, tipo_variacao_id, imagem, modelo_produto_id, outras_informacoes) VALUES(26, '2021-06-26 21:00:00.000', '2021-06-26 21:00:00.000', 4, NULL, 3, NULL);
INSERT INTO modelo_variacao (id, created_at, updated_at, tipo_variacao_id, imagem, modelo_produto_id, outras_informacoes) VALUES(27, '2021-06-26 21:00:00.000', '2021-06-26 21:00:00.000', 5, NULL, 3, NULL);
INSERT INTO modelo_variacao (id, created_at, updated_at, tipo_variacao_id, imagem, modelo_produto_id, outras_informacoes) VALUES(28, '2021-06-26 21:00:00.000', '2021-06-26 21:00:00.000', 6, NULL, 3, NULL);
INSERT INTO modelo_variacao (id, created_at, updated_at, tipo_variacao_id, imagem, modelo_produto_id, outras_informacoes) VALUES(29, '2021-06-26 21:00:00.000', '2021-06-26 21:00:00.000', 8, NULL, 3, NULL);
INSERT INTO modelo_variacao (id, created_at, updated_at, tipo_variacao_id, imagem, modelo_produto_id, outras_informacoes) VALUES(30, '2021-06-26 21:00:00.000', '2021-06-26 21:00:00.000', 8, NULL, 4, NULL);
INSERT INTO modelo_variacao (id, created_at, updated_at, tipo_variacao_id, imagem, modelo_produto_id, outras_informacoes) VALUES(31, '2021-06-26 21:00:00.000', '2021-06-26 21:00:00.000', 3, NULL, 4, NULL);
INSERT INTO modelo_variacao (id, created_at, updated_at, tipo_variacao_id, imagem, modelo_produto_id, outras_informacoes) VALUES(32, '2021-06-26 21:00:00.000', '2021-06-26 21:00:00.000', 4, NULL, 4, NULL);
INSERT INTO modelo_variacao (id, created_at, updated_at, tipo_variacao_id, imagem, modelo_produto_id, outras_informacoes) VALUES(33, '2021-06-26 21:00:00.000', '2021-06-26 21:00:00.000', 5, NULL, 4, NULL);
INSERT INTO modelo_variacao (id, created_at, updated_at, tipo_variacao_id, imagem, modelo_produto_id, outras_informacoes) VALUES(34, '2021-06-26 21:00:00.000', '2021-06-26 21:00:00.000', 6, NULL, 4, NULL);
INSERT INTO modelo_variacao (id, created_at, updated_at, tipo_variacao_id, imagem, modelo_produto_id, outras_informacoes) VALUES(35, '2021-06-26 21:00:00.000', '2021-06-26 21:00:00.000', 8, NULL, 5, NULL);
INSERT INTO modelo_variacao (id, created_at, updated_at, tipo_variacao_id, imagem, modelo_produto_id, outras_informacoes) VALUES(36, '2021-06-26 21:00:00.000', '2021-06-26 21:00:00.000', 3, NULL, 5, NULL);
INSERT INTO modelo_variacao (id, created_at, updated_at, tipo_variacao_id, imagem, modelo_produto_id, outras_informacoes) VALUES(37, '2021-06-26 21:00:00.000', '2021-06-26 21:00:00.000', 4, NULL, 5, NULL);
INSERT INTO modelo_variacao (id, created_at, updated_at, tipo_variacao_id, imagem, modelo_produto_id, outras_informacoes) VALUES(38, '2021-06-26 21:00:00.000', '2021-06-26 21:00:00.000', 5, NULL, 5, NULL);
INSERT INTO modelo_variacao (id, created_at, updated_at, tipo_variacao_id, imagem, modelo_produto_id, outras_informacoes) VALUES(39, '2021-06-26 21:00:00.000', '2021-06-26 21:00:00.000', 6, NULL, 5, NULL);
INSERT INTO modelo_variacao (id, created_at, updated_at, tipo_variacao_id, imagem, modelo_produto_id, outras_informacoes) VALUES(40, '2021-06-26 21:00:00.000', '2021-06-26 21:00:00.000', 8, NULL, 6, NULL);
INSERT INTO modelo_variacao (id, created_at, updated_at, tipo_variacao_id, imagem, modelo_produto_id, outras_informacoes) VALUES(41, '2021-06-26 21:00:00.000', '2021-06-26 21:00:00.000', 3, NULL, 6, NULL);
INSERT INTO modelo_variacao (id, created_at, updated_at, tipo_variacao_id, imagem, modelo_produto_id, outras_informacoes) VALUES(42, '2021-06-26 21:00:00.000', '2021-06-26 21:00:00.000', 4, NULL, 6, NULL);
INSERT INTO modelo_variacao (id, created_at, updated_at, tipo_variacao_id, imagem, modelo_produto_id, outras_informacoes) VALUES(43, '2021-06-26 21:00:00.000', '2021-06-26 21:00:00.000', 5, NULL, 6, NULL);
INSERT INTO modelo_variacao (id, created_at, updated_at, tipo_variacao_id, imagem, modelo_produto_id, outras_informacoes) VALUES(44, '2021-06-26 21:00:00.000', '2021-06-26 21:00:00.000', 6, NULL, 6, NULL);
INSERT INTO modelo_variacao (id, created_at, updated_at, tipo_variacao_id, imagem, modelo_produto_id, outras_informacoes) VALUES(45, '2021-06-26 21:00:00.000', '2021-06-26 21:00:00.000', 8, NULL, 7, NULL);
INSERT INTO modelo_variacao (id, created_at, updated_at, tipo_variacao_id, imagem, modelo_produto_id, outras_informacoes) VALUES(46, '2021-06-26 21:00:00.000', '2021-06-26 21:00:00.000', 3, NULL, 7, NULL);
INSERT INTO modelo_variacao (id, created_at, updated_at, tipo_variacao_id, imagem, modelo_produto_id, outras_informacoes) VALUES(47, '2021-06-26 21:00:00.000', '2021-06-26 21:00:00.000', 4, NULL, 7, NULL);
INSERT INTO modelo_variacao (id, created_at, updated_at, tipo_variacao_id, imagem, modelo_produto_id, outras_informacoes) VALUES(48, '2021-06-26 21:00:00.000', '2021-06-26 21:00:00.000', 5, NULL, 7, NULL);
INSERT INTO modelo_variacao (id, created_at, updated_at, tipo_variacao_id, imagem, modelo_produto_id, outras_informacoes) VALUES(49, '2021-06-26 21:00:00.000', '2021-06-26 21:00:00.000', 6, NULL, 7, NULL);
INSERT INTO modelo_variacao (id, created_at, updated_at, tipo_variacao_id, imagem, modelo_produto_id, outras_informacoes) VALUES(50, '2021-07-19 13:34:22.381', '2021-07-19 13:34:22.381', 8, NULL, 8, NULL);
INSERT INTO modelo_variacao (id, created_at, updated_at, tipo_variacao_id, imagem, modelo_produto_id, outras_informacoes) VALUES(51, '2021-07-19 13:34:22.396', '2021-07-19 13:34:22.396', 3, NULL, 8, NULL);
INSERT INTO modelo_variacao (id, created_at, updated_at, tipo_variacao_id, imagem, modelo_produto_id, outras_informacoes) VALUES(52, '2021-07-19 13:34:22.405', '2021-07-19 13:34:22.405', 4, NULL, 8, NULL);
INSERT INTO modelo_variacao (id, created_at, updated_at, tipo_variacao_id, imagem, modelo_produto_id, outras_informacoes) VALUES(53, '2021-07-19 13:34:22.413', '2021-07-19 13:34:22.413', 5, NULL, 8, NULL);
INSERT INTO modelo_variacao (id, created_at, updated_at, tipo_variacao_id, imagem, modelo_produto_id, outras_informacoes) VALUES(54, '2021-07-19 13:34:22.420', '2021-07-19 13:34:22.421', 6, NULL, 8, NULL);
INSERT INTO modelo_variacao (id, created_at, updated_at, tipo_variacao_id, imagem, modelo_produto_id, outras_informacoes) VALUES(55, '2021-08-04 23:22:56.983', '2021-08-04 23:22:56.983', 8, NULL, 9, NULL);
INSERT INTO modelo_variacao (id, created_at, updated_at, tipo_variacao_id, imagem, modelo_produto_id, outras_informacoes) VALUES(56, '2021-08-04 23:22:56.993', '2021-08-04 23:22:56.993', 3, NULL, 9, NULL);
INSERT INTO modelo_variacao (id, created_at, updated_at, tipo_variacao_id, imagem, modelo_produto_id, outras_informacoes) VALUES(57, '2021-08-04 23:22:56.995', '2021-08-04 23:22:56.995', 4, NULL, 9, NULL);
INSERT INTO modelo_variacao (id, created_at, updated_at, tipo_variacao_id, imagem, modelo_produto_id, outras_informacoes) VALUES(58, '2021-08-04 23:22:56.996', '2021-08-04 23:22:56.996', 5, NULL, 9, NULL);
INSERT INTO modelo_variacao (id, created_at, updated_at, tipo_variacao_id, imagem, modelo_produto_id, outras_informacoes) VALUES(59, '2021-08-04 23:22:56.998', '2021-08-04 23:22:56.998', 6, NULL, 9, NULL);
INSERT INTO modelo_variacao (id, created_at, updated_at, tipo_variacao_id, imagem, modelo_produto_id, outras_informacoes) VALUES(60, '2021-08-04 23:22:57.702', '2021-08-04 23:22:57.702', 9, 'image/upload/v1628130177/p0fr7qetvxuhib2kfedg.png', 9, NULL);
INSERT INTO modelo_produto (id, created_at, updated_at, produto_id, modelo_id) VALUES(1, '2021-06-25 21:00:00.000', '2021-06-25 21:00:00.000', 19, 1);
INSERT INTO modelo_produto (id, created_at, updated_at, produto_id, modelo_id) VALUES(2, '2021-06-26 21:00:00.000', '2021-06-26 21:00:00.000', 20, 1);
INSERT INTO modelo_produto (id, created_at, updated_at, produto_id, modelo_id) VALUES(3, '2021-06-26 21:00:00.000', '2021-06-26 21:00:00.000', 18, 1);
INSERT INTO modelo_produto (id, created_at, updated_at, produto_id, modelo_id) VALUES(4, '2021-06-26 21:00:00.000', '2021-06-26 21:00:00.000', 17, 1);
INSERT INTO modelo_produto (id, created_at, updated_at, produto_id, modelo_id) VALUES(5, '2021-06-26 21:00:00.000', '2021-06-26 21:00:00.000', 21, 1);
INSERT INTO modelo_produto (id, created_at, updated_at, produto_id, modelo_id) VALUES(6, '2021-06-26 21:00:00.000', '2021-06-26 21:00:00.000', 1, 1);
INSERT INTO modelo_produto (id, created_at, updated_at, produto_id, modelo_id) VALUES(7, '2021-06-26 21:00:00.000', '2021-06-26 21:00:00.000', 5, 1);
INSERT INTO modelo_produto (id, created_at, updated_at, produto_id, modelo_id) VALUES(8, '2021-07-19 13:34:22.369', '2021-07-19 13:34:22.369', 22, 1);
INSERT INTO modelo_produto (id, created_at, updated_at, produto_id, modelo_id) VALUES(9, '2021-08-04 23:22:56.975', '2021-08-04 23:22:56.975', 23, 2);

