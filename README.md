# Chess Socket

Chess Socket é um jogo de xadrez do tipo cliente-servidor que utiliza o protocolo TCP para comunicação entre os jogadores. Este repositório contém o código-fonte tanto do cliente quanto do servidor.

## Funcionamento

O servidor é executado em uma máquina, enquanto os clientes podem ser executados em outras máquinas conectadas à mesma rede. Quando um cliente se conecta ao servidor, ele pode criar ou se juntar a uma partida de xadrez em andamento. Os movimentos dos jogadores são transmitidos através do protocolo TCP, permitindo que ambos os jogadores vejam o tabuleiro atualizado em tempo real.

O servidor é capaz de hospedar várias partidas simultaneamente, cada uma com dois jogadores. Quando uma partida é concluída, o resultado é exibido para ambos os jogadores e eles podem optar por jogar novamente ou sair do jogo.

## Instalação

Para executar o Chess Socket, você precisará do Python 3.1 ou superior instalado em sua máquina.

1. Clone o repositório do Chess Socket em sua máquina local.
2. Instale as dependências necessárias, executando o seguinte comando na raiz do projeto:

`pip install -r requirements.txt`  

3. Execute o servidor executando o seguinte comando:

`python server.py`

4. Execute o cliente executando o seguinte comando:

`python client.py`

## Utilização  

Para iniciar uma partida, um dos jogadores deve criar uma nova partida e aguardar até que outro jogador se junte à partida. Depois que ambos os jogadores se conectarem, a partida começará automaticamente.

Durante a partida, cada jogador pode mover suas peças clicando na peça que deseja mover e, em seguida, clicando no local para onde deseja movê-la. Se uma jogada for inválida, o movimento será revertido e o jogador deverá tentar novamente.

Quando um jogador captura o rei do oponente, a partida é encerrada e o resultado é exibido para ambos os jogadores. Eles podem optar por jogar novamente ou sair do jogo.

## Contribuindo

Se você deseja contribuir com o Chess Socket, fique à vontade para abrir uma solicitação de pull ou uma issue no repositório. Teremos prazer em revisar sua contribuição e integrá-la ao projeto.
