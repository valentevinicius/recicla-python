## Importação de bibliotecas
import os
from math import radians, cos, sin, asin, sqrt

## Constantes
OPCAO_VOLTAR = 'VOLTAR'

## Exibe o menu principal da aplicação (solicita ao usuário a escolha de uma categoria)
def exibeMenuInicial():
    ## http://patorjk.com/software/taag (converte texto para ASCII)
    print(
    r"""
    ______          _      _             
    | ___ \        (_)    | |        _   
    | |_/ /___  ___ _  ___| | __ _ _| |_ 
    |    // _ \/ __| |/ __| |/ _` |_   _|
    | |\ \  __/ (__| | (__| | (_| | |_|  
    \_| \_\___|\___|_|\___|_|\__,_|       
    """)
    print(
        """O objetivo deste programa é facilitar o processo de reciclagem, desde a identificação do reciclável até a localização de um ponto para coleta. É tudo muito fácil, vamos começar!?\n""")
    print(
        """Digite o número de uma categoria abaixo:
        
        [1] - Plástico
        [2] - Metal
        [3] - Vidro
        [4] - Papel
        [5] - Eletrônicos
        [6] - Encerrar o programa"""
    )

## Obtem um array/vetor contendo o número das categorias disponíveis
def getOpcoesCategorias():
    return [ 1, 2, 3, 4, 5, 6, 7 ]

## Obtem um array/vetor contendo o número das opções disponíveis de uma dada lista de objetos
def getOpcoesByObjetos(objetos):
    opcoesDisponiveis = []

    for objeto in objetos:
        opcoesDisponiveis.append(objeto['id'])

    return opcoesDisponiveis

## Converte uma opção de menu (1, 2, 3, etc.) para um tipo específico (papel, vidro, etc.)
def convertOpcaoToTipo(opcao):
    if opcao == 1:
        return 'plastico'
    elif opcao == 2:
        return 'metal'
    elif opcao == 3:
        return 'vidro'
    elif opcao == 4:
        return 'papel'
    elif opcao == 5:
        return 'eletronico'
    elif opcao == 6:
        return 'outro'
    else:
        return ''

## Retorna os pontos de coleta a partir de uma categoria (plástico, vidro, papel, etc.)
def getPontosDeColetaByCategoria(categoria):
    pontosDeColeta = []

    for ponto in getPontosDeColeta():
        for categoriaPonto in ponto['categorias']:
            if categoriaPonto == categoria:
                pontosDeColeta.append(ponto)

    return pontosDeColeta

## Retorna um array/vetor contendo os objetos disponíveis para serem reciclados baseado num tipo específico (plástico, vidro, etc.)
def getObjetosByTipo(opcao):
    objetos = []
    tipo = convertOpcaoToTipo(opcao)

    for objeto in getObjetos():
        if objeto['tipo'] == tipo:
            objetos.append(objeto)

    return objetos

## Retorna um objeto realizando uma busca em uma dada lista e por um dado id
def getObjetoById(objetos, id):
    for objeto in objetos:
        if objeto['id'] == id:
            return objeto

## Retorna o ponto de coleta mais próximo (se baseia na latitude e longitude do usuário)
def getPontosDeColetaMaisProximo(pontosDeColeta, latitude, longitude, distMax):
    pontoMaisProximo = pontosDeColeta[0]
    pontos = []

    pontoMaisProximo['distancia'] = 0

    for ponto in pontosDeColeta:
        lon1 = longitude
        lat1 = latitude
        lon2 = ponto['longitude']
        lat2 = ponto['latitude']
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

        # Haversine
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        r = 6371
        distancia = c*r
        distancia = round(distancia, 3)
        ponto['distancia'] = distancia

        if (ponto['distancia'] < distMax):
            pontos.append(ponto)
        
        if ponto['distancia'] < pontoMaisProximo['distancia']:
            pontoMaisProximo = ponto

    ## Caso não exista nenhum ponto de coleta dentro do raio de distância, retorne o mais próximo
    if len(pontos) == 0:
        pontos.append(pontoMaisProximo)

    return pontos

## Exibe o banco de objetos a partir de uma opção escolhida (plástico, vidro, etc.)
def exibeObjetosByOpcao(numeroOpcao):
    ## Variáveis
    objetos = getObjetosByTipo(numeroOpcao)
    opcoesDisponiveis = getOpcoesByObjetos(objetos)
    opcaoEscolhida = 0
    opcaoValida = False
    objetoEscolhido = {}

    ## Solicita ao usuário escolher um objeto a ser reciclado 
    while not(opcaoValida):
        limpaConsole()

        print('Exibindo os materiais recicláveis para a categoria informada..\n')

        for objeto in objetos:
            print("""   * """ + '[{id}] - {nome}'.format(id = objeto['id'], nome = objeto['descricao']))

        print('\nNOTA: Se quiser voltar para o menu inicial, digite a palavra VOLTAR ;)')

        opcaoEscolhida = input('\nDigite o nº do objeto que deseja reciclar: ')

        ## Converte para inteiro (int) caso o usuário tenha digitado somente números
        opcaoEscolhida = int(opcaoEscolhida) if opcaoEscolhida.isnumeric() else str(opcaoEscolhida)

        if opcoesDisponiveis.count(opcaoEscolhida):
            opcaoValida = True
            objetoEscolhido = getObjetoById(objetos, opcaoEscolhida)
        elif str(opcaoEscolhida).upper() == OPCAO_VOLTAR:
            ## Volta para o menu inicial
            return True
        else:
            opcaoValida = False
            exibeMensagemErro('Opção inexistente. Tente novamente.')
    
    ## Reseta variável 'opcaoValida'
    opcaoValida = False

    ## Exibe os detalhes do objeto e solicita a localização (coordenadas) do usuário
    while not(opcaoValida):
        ## Variáveis
        latitude = ''
        longitude = ''
        pontosDeColetaDisponiveis = getPontosDeColetaByCategoria(objetoEscolhido['tipo'])
        pontosDeColetaMaisProximos = {}

        limpaConsole()

        print('Dados do material a ser reciclado:\n')
        
        exibeDetalhesObjeto(objetoEscolhido)
    
        print('\nAgora iremos precisar que você digite as suas coordenadas geográficas (latitude e longitude), ok? (Dica: você pode digitar a palavra UNIP que iremos considerar a localização da UNIP - Swift)\n')
        
        latitude = str(input('Digite a sua latitude: '))
        longitude = str(input('Digite a sua longitude: '))

        distMax = digiteDistancia()

        if len(latitude) > 0 and len(longitude):
            ## Considera latitude e longitude da UNIP
            latitude = -22.926301 if latitude.upper() == 'UNIP' else latitude
            longitude = -47.037686 if longitude.upper() == 'UNIP' else longitude

            try:
                latitude = float(latitude)
                longitude = float(longitude)
                distMax = float(distMax)

                opcaoValida = True
            
                pontosDeColetaMaisProximos = getPontosDeColetaMaisProximo(pontosDeColetaDisponiveis, latitude, longitude, distMax)
                
                limpaConsole()

                if pontosDeColetaMaisProximos[0]['distancia'] <= distMax:
                    print('Esses são os pontos correspondentes com sua busca: \n')
                    
                    for ponto in pontosDeColetaMaisProximos :
                        print('Distância: ', format(ponto['distancia'], '.2f'), ' Km\nNome: ', ponto['nome'], '\nEndereço: ', ponto['endereco'], '\n')
                else:
                    print(f'Não encontramos nenhum ponto de coleta no raio de {distMax:.2f} km. O local mais próximo encontra-se logo abaixo: ')
                    print('\nDistância: ', format(pontosDeColetaMaisProximos[0]['distancia'], '.2f'), ' Km\nNome: ', pontosDeColetaMaisProximos[0]['nome'], '\nEndereço: ', pontosDeColetaMaisProximos[0]['endereco'], '\n')

                input('\nPrecione qualquer tecla para voltar ao menu inicial!\n')
            except:
                opcaoValida = False
                exibeMensagemErro('Certifique-se de digitar os dados corretamente.')
        else:
            opcaoValida = False
            exibeMensagemErro('Certifique-se de digitar os dados corretamente.')
    
    ## Retorna True, assim redireciona o usário para o menu inicial da aplicação
    return True

## Exibe os detalhes do objeto a ser reciclado
def exibeDetalhesObjeto(objeto):
    print("""  => Código interno..........: """ + str(objeto['id']))
    print("""  => Material a ser reciclado: """ + str(objeto['descricao']))

## Solicita ao usuário a distância máxima que ele está disposto a percorrer
def digiteDistancia():
    return input('Digite a distância máxima (em KM) que você está disposto a percorrer pelo ponto --> ')

## Exibe uma mensagem de erro no console
def exibeMensagemErro(msg):
    limpaConsole()
    print('Ops... Algo deu errado :(')
    print('[ERRO] => ' + str(msg))
    print('\nPrecione qualquer tecla para continuar')
    input()
    
## Limpa o console
def limpaConsole():
    os.system('cls') ## Executa o comando 'cls' no console

## Retorna um array/vetor contendo todos os objetos disponíveis para serem reciclados
def getObjetos():
    return  [
        { 'id': 1, 'descricao': 'Garrafa PET', 'obs': '', 'tipo': 'plastico', },
        { 'id': 2, 'descricao': 'Potes de plástico', 'obs': '', 'tipo': 'plastico' },
        { 'id': 3, 'descricao': 'Tampa de embalagem', 'obs': '', 'tipo': 'plastico' },
        { 'id': 4, 'descricao': 'Cano PVC', 'obs': '', 'tipo': 'plastico' },
        { 'id': 5, 'descricao': 'Saco plástico', 'obs': '', 'tipo': 'plastico' },
        { 'id': 6, 'descricao': 'Peça de brinquedo', 'obs': '', 'tipo': 'plastico' },
        { 'id': 7, 'descricao': 'Balde', 'obs': '', 'tipo': 'plastico' },
        { 'id': 8, 'descricao': 'Lata de alumínio', 'obs': '', 'tipo': 'metal' },
        { 'id': 9, 'descricao': 'Lata de aço', 'obs': '', 'tipo': 'metal' },
        { 'id': 10, 'descricao': 'Tampa', 'obs': '', 'tipo': 'metal' },
        { 'id': 11, 'descricao': 'Ferragem', 'obs': '', 'tipo': 'metal' },
        { 'id': 12, 'descricao': 'Cano', 'obs': '', 'tipo': 'metal' },
        { 'id': 13, 'descricao': 'Moldura de quadro', 'obs': '', 'tipo': 'metal' },
        { 'id': 14, 'descricao': 'Garrafa de vidro', 'obs': '', 'tipo': 'vidro' },
        { 'id': 15, 'descricao': 'Pote de conserva', 'obs': '', 'tipo': 'vidro' },
        { 'id': 16, 'descricao': 'Frascos de vidro', 'obs': '', 'tipo': 'vidro' },
        { 'id': 17, 'descricao': 'Copo de vidro', 'obs': '', 'tipo': 'vidro' },
        { 'id': 18, 'descricao': 'Vidro de janela', 'obs': '', 'tipo': 'vidro' },
        { 'id': 19, 'descricao': 'Jornal', 'obs': '', 'tipo': 'papel' },
        { 'id': 20, 'descricao': 'Revista', 'obs': '', 'tipo': 'papel' },
        { 'id': 21, 'descricao': 'Envelope', 'obs': '', 'tipo': 'papel' },
        { 'id': 22, 'descricao': 'Caderno', 'obs': '', 'tipo': 'papel' },
        { 'id': 23, 'descricao': 'Caixa de papelão', 'obs': '', 'tipo': 'papel' },
        { 'id': 24, 'descricao': 'Embalagem longa vida', 'obs': '', 'tipo': 'papel' },
        { 'id': 25, 'descricao': 'Cartaz', 'obs': '', 'tipo': 'papel' },
        { 'id': 26, 'descricao': 'Monitor de computador', 'obs': '', 'tipo': 'eletronico' },
        { 'id': 27, 'descricao': 'Telefone celular (smartphone)', 'obs': '', 'tipo': 'eletronico' },
        { 'id': 28, 'descricao': 'Bateria / pilha', 'obs': '', 'tipo': 'eletronico' },
        { 'id': 29, 'descricao': 'Computador (notebook ou desktop)', 'obs': '', 'tipo': 'eletronico' },
        { 'id': 30, 'descricao': 'DVD Player', 'obs': '', 'tipo': 'eletronico' },
        { 'id': 31, 'descricao': 'Impressora', 'obs': '', 'tipo': 'eletronico' },
        { 'id': 32, 'descricao': 'Câmera fotográfica', 'obs': '', 'tipo': 'eletronico' }
    ]

## Retorna um array/vetor contendo todos os pontos de coleta disponíveis
def getPontosDeColeta():
    return [
        { 'id': 1, 'nome': 'Ponto Verde - Vila Costa e Silva', 'endereco': 'R. Saldanha da Gama, 77 - Vila Costa e Silva, Campinas - SP, 13081-000', 'latitude': -22.856155, 'longitude': -47.068549, 'categorias': ['plastico'] },
        { 'id': 2, 'nome': 'Ecoponto Jardim Pacaembu', 'endereco': 'R. Dante Suriani, 2-382 - Chácara Cneo, Campinas - SP, 13033-160', 'latitude': -22.904529, 'longitude': -47.105434, 'categorias': ['plastico'] },
        { 'id': 3, 'nome': 'HT Papéis Barão - Coleta e reciclagem de resíduos', 'endereco': 'Av. Ruy Rodrigues, 394 - Jardim Novo Campos Eliseos, Campinas - SP, 13060-192', 'latitude': -22.934023, 'longitude': -47.105661, 'categorias': ['plastico', 'papel'] },
        { 'id': 5, 'nome': 'Ecoponto Vila União', 'endereco': 'R. Manoel Gomes Ferreira, 42 - Parque Tropical, Campinas - SP, 13060-523', 'latitude': -22.936016, 'longitude': -47.118061, 'categorias': ['plastico'] },
        { 'id': 6, 'nome': 'Ecoponto / Ponto Verde', 'endereco': 'Av. Santa Isabel, 2300 - Barão Geraldo, Campinas - SP, 13084-012', 'latitude': -22.817244, 'longitude': -47.100531, 'categorias': ['papel'] },
        { 'id': 7, 'nome': 'GMV Recycle', 'endereco': 'Rod. Lix da Cunha, 911 - Jardim Nova America, Campinas - SP, 13070-715', 'latitude': -22.898166, 'longitude': -47.093476, 'categorias': ['papel', 'eletronico'] },
        { 'id': 8, 'nome': 'Ecoponto Jardim Eulina',  'endereco': 'Av. Mal. Rondon, 2296-2382 - Jardim Chapadão, Campinas - SP', 'latitude': -22.891751, 'longitude': -47.100940, 'categorias': ['papel', 'vidro', 'plastico', 'metal'] },
        { 'id': 9, 'nome': 'Reversis - Reciclagem de Eletrônicos e Informática',  'endereco': 'R. da Abolição, 1900 - Pte. Preta, Campinas - SP, 13041-445', 'latitude': -22.926823, 'longitude': -47.042984, 'categorias': ['eletronico'] },
        { 'id': 10, 'nome': 'Cooperativa de Recicláveis Santa Genebra',  'endereco': 'R. Estácio de Sá, 577 - Jardim Santa Genebra, Campinas - SP, 13084-751', 'latitude': -22.852778, 'longitude': -47.074819, 'categorias': ['papel', 'vidro', 'plastico', 'metal'] }
    ]
