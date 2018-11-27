import argparse
from readers.read_blast import BlastReader

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--test', '-t',
                        help='Caminho para arquivo BLAST de teste',
                        required=True)
arg_parser.add_argument('--ref', '-r',
                        help='Caminho para arquivo BLAST de referencia',
                        required=True)
ARGS = arg_parser.parse_args()


BLAST_PATH_TEST = ARGS.test
BLAST_PATH_REF = ARGS.ref


def calcula_medidas():
    blast_reader_test = BlastReader(BLAST_PATH_TEST)
    blast_reader_ref = BlastReader(BLAST_PATH_REF)

    verdadeiro_positivo = 0
    falso_positivo = 0
    for (idx, error) in blast_reader_test.error_lines:
        error_type = error[-1]
        sys_idxs = error[1]

        fp = 1
        for (idx2, error2) in blast_reader_ref.get_filtered_errors([error_type]):
            if idx2 == idx:
                if set(sys_idxs) & set(error2[1]):
                    verdadeiro_positivo += 1
                    fp = 0
                    break
        falso_positivo += fp

    falso_negativo = 0
    for (idx, error) in blast_reader_ref.error_lines[:10]:
        error_type = error[-1]
        sys_idxs = error[1]

        fn = 1
        for (idx2, error2) in blast_reader_test.get_filtered_errors([error_type]):
            if idx2 == idx:
                if set(sys_idxs) & set(error2[1]):
                    fn = 0
                    break
        falso_negativo += fn

    precisao = verdadeiro_positivo / (verdadeiro_positivo + falso_positivo)
    cobertura = verdadeiro_positivo / (verdadeiro_positivo + falso_negativo)

    print('Precisao: {}'.format(precisao))
    print('Cobertura: {}'.format(cobertura))

if __name__ == "__main__":
    calcula_medidas()