# def calculator_rating():
    
#     jogador_a = 1600 #jogador_a é o rating atual do jogador A
#     jogador_b = 1800 #jogador_b é o rating atual do jogador B
    
#     k = 20
#     # O fator K determina o máximo de pontos que um jogador pode ganhar ou perder em uma única partida. Ele varia dependendo do rating do jogador e da organização:
#     # K = 40 para um novo jogador até sua 30ª partida avaliada
#     # K = 20 para ratings abaixo de 2400
#     # K = 10 para ratings de 2400 e acima
    
#     result = 1 #result é o resultado da partida (1 para vitória, 0.5 para empate, 0 para derrota)
    
#     #Cálculo da Expectativa de Vitória
#     #E1 é a expectativa de vitória do jogador A
#     E1 = 1 / (1 + 10 ** ((jogador_b - jogador_a) / 400))
#     print("Expectativa de vitória jogador A: ", E1)

#     E2 = 1 / (1 + 10 ** ((jogador_a - jogador_b) / 400))
#     print("Expectativa de vitória jogador B: ", E2)

#     # Cálculo Atualização do Rating jogador A
#     rating_novo = jogador_a + k * (0.5 - E1) #Supondo empate
#     result_a = rating_novo
#     print(f"O rating novo do jogador A é:  {result_a:.1f}")

#     # Cálculo Atualização do Rating jogador B
#     rating_novo = jogador_b + k * (0.5 - E2) #Supondo empate
#     result_b = rating_novo
#     print(f"O rating novo do jogador B é:  {result_b:.1f}")

# calculator_rating()


# # def calcular_rating():
# #         jogador1 = 1600 #jogador_a é o rating atual do jogador A
# #         jogador2 = 1800 #jogador_b é o rating atual do jogador B
        
# #         K = 32  
        
# #         # Cálculo da expectativa de vitória
# #         R1 = 10 ** (jogador1 / 400)
# #         R2 = 10 ** (jogador2 / 400)
        
# #         E1 = R1 / (R1 + R2)
        
# #         print(E1)

# # calcular_rating()

    