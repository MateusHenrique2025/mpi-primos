from mpi4py import MPI

def contar_primos(inicio, fim):
    cont = 0
    for n in range(max(inicio, 2), fim + 1):
        i = 2
        while i * i <= n:
            if n % i == 0:
                break
            i += 1
        else:
            cont += 1
    return cont

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

intervalo_max = 2_000_000

t0 = MPI.Wtime()

# Divisão do trabalho
tamanho_bloco = intervalo_max // size
inicio = rank * tamanho_bloco + 1
fim = intervalo_max if rank == size - 1 else inicio + tamanho_bloco - 1

primos = contar_primos(inicio, fim)

if rank != 0:
    comm.send(primos, dest=0)           # Trabalhador envia
else:
    total = primos
    for i in range(1, size):
        total += comm.recv(source=i)    # Mestre coleta
    print(f"Total de primos ate {intervalo_max}: {total}")
    print(f"Tempo com {size} processo(s): {MPI.Wtime() - t0:.2f} s")