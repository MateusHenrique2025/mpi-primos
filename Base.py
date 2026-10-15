from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()  # Quem sou eu?
size = comm.Get_size()  # Quantos somos?

# Definição do valor máximo do intervalo para exemplo
intervalo_max = 100

# Divisão do trabalho:
tamanho_bloco = intervalo_max // size
inicio = rank * tamanho_bloco + 1
fim = (rank + 1) * tamanho_bloco if rank < size - 1 else intervalo_max

print(f"Processo {rank} de {size}: intervalo de {inicio} até {fim}")