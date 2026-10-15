from mpi4py import MPI

INTERVALO_MAX = 2_000_000


def primos_base(limite):
    crivo = bytearray([1]) * (limite + 1)
    crivo[0:2] = b"\x00\x00"
    for i in range(2, int(limite ** 0.5) + 1):
        if crivo[i]:
            crivo[i * i :: i] = bytearray(len(range(i * i, limite + 1, i)))
    return [i for i in range(2, limite + 1) if crivo[i]]


def contar_primos(inicio, fim):
    if fim < 2 or inicio > fim:
        return 0
    inicio = max(inicio, 2)
    segmento = bytearray([1]) * (fim - inicio + 1)
    for p in primos_base(int(fim ** 0.5) + 1):
        primeiro = max(p * p, ((inicio + p - 1) // p) * p)
        if primeiro > fim:
            continue
        segmento[primeiro - inicio :: p] = bytearray(len(range(primeiro, fim + 1, p)))
    return sum(segmento)


def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    tempo_inicial = MPI.Wtime()

    tamanho_bloco = INTERVALO_MAX // size
    inicio = rank * tamanho_bloco + 1
    fim = INTERVALO_MAX if rank == size - 1 else inicio + tamanho_bloco - 1

    primos = contar_primos(inicio, fim)
    print(f"Processo {rank}: [{inicio}, {fim}] -> {primos} primos")

    if rank != 0:
        comm.send(primos, dest=0)
    else:
        total = primos
        for i in range(1, size):
            total += comm.recv(source=i)
        tempo = MPI.Wtime() - tempo_inicial
        print(f"Total de primos de 1 a {INTERVALO_MAX}: {total}")
        print(f"Tempo: {tempo:.3f} s com {size} processo(s)")


if __name__ == "__main__":
    main()
