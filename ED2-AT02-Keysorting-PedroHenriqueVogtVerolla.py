import sys

class Hero:
    def __init__(self, key, nome, lado, genero, corOlho, raca, corCabelo, publisher, corPele, altura, peso, inteligencia, forca, velocidade, resistencia, poder, combate, total):
        # transforma tudo o que é string pra numero
        def convertePraNumero(valor, default=-1):
            try:
                if valor == '-' or valor.strip() == '':
                    return default
                return int(float(valor))
            except (ValueError, TypeError):
                return default  #retorna -1 se o intput for invalido
        
        self.key = convertePraNumero(key)
        self.nome = nome
        self.lado = lado
        self.genero = genero
        self.corOlho = corOlho
        self.raca = raca
        self.corCabelo = corCabelo
        self.publisher = publisher
        self.corPele = corPele
        self.altura = convertePraNumero(altura)
        self.peso = convertePraNumero(peso)
        self.inteligencia = convertePraNumero(inteligencia)
        self.forca = convertePraNumero(forca)
        self.velocidade = convertePraNumero(velocidade)
        self.resistencia = convertePraNumero(resistencia)
        self.poder = convertePraNumero(poder)
        self.combate = convertePraNumero(combate)
        self.total = convertePraNumero(total)

    def to_string(self):
        #converte o objeto pra string limitando por | 
        return f"{self.key}|{self.nome}|{self.lado}|{self.genero}|{self.corOlho}|{self.raca}|{self.corCabelo}|{self.publisher}|{self.corPele}|{self.altura}|{self.peso}|{self.inteligencia}|{self.forca}|{self.velocidade}|{self.resistencia}|{self.poder}|{self.combate}|{self.total}"

#SORTINGS
def insertion_sort(arr, ordem):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and ((ordem == 'C' and arr[j].key > key.key) or (ordem == 'D' and arr[j].key < key.key)):
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

def merge_sort(arr, ordem):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid], ordem)
    right = merge_sort(arr[mid:], ordem)
    return merge(left, right, ordem)

def merge(left, right, ordem):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if (ordem == 'C' and left[i].key <= right[j].key) or (ordem == 'D' and left[i].key >= right[j].key):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def quick_sort(arr, ordem):
    def _quick_sort(arr, low, high):
        if low < high:
            pi = partition(arr, low, high, ordem)
            _quick_sort(arr, low, pi - 1)
            _quick_sort(arr, pi + 1, high)
        return arr
    
    def partition(arr, low, high, ordem):
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if (ordem == 'C' and arr[j].key <= pivot.key) or (ordem == 'D' and arr[j].key >= pivot.key):
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1
    
    return _quick_sort(arr, 0, len(arr) - 1)

def heap_sort(arr, ordem):
    def heapify(arr, n, i, ordem):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        if left < n and ((ordem == 'C' and arr[left].key > arr[largest].key) or (ordem == 'D' and arr[left].key < arr[largest].key)):
            largest = left
        if right < n and ((ordem == 'C' and arr[right].key > arr[largest].key) or (ordem == 'D' and arr[right].key < arr[largest].key)):
            largest = right
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            heapify(arr, n, largest, ordem)
    
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i, ordem)
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(arr, i, 0, ordem)
    return arr

#função que extrai as informacoes da primeira linha do arquivo
def leHeader(header):
    parametros = header.strip().split(',')
    metodoSort = None
    ordem = None
    for param in parametros:
        key, valor = param.strip().split('=')
        if key == 'SORT':
            metodoSort = valor
        elif key == 'ORDER':
            ordem = valor
    if metodoSort not in ['Q', 'M', 'H', 'I'] or ordem not in ['C', 'D']:
        raise ValueError("Parametros invalidos")
    return metodoSort, ordem

#lendo o input
def leInput(filename):
    try:
        with open(filename, 'r') as f:
            linhas = f.readlines()
            if len(linhas) < 2:
                raise ValueError("Input vazio ou incompleto")
            
            metodoSort, ordem = leHeader(linhas[0])
            campos = linhas[1].strip().split('|')
            if len(campos) < 18: #tem 18 campos
                raise ValueError("Input ta com as colunas erradas")
            
            # Parse hero records
            herois = []
            for i, line in enumerate(linhas[2:], start=3):
                if line.strip():
                    data = line.strip().split('|')
                    if len(data) < 18:
                        print(f"Erro na linha {i}: {line.strip()}")
                        continue
                    try:
                        herois.append(Hero(*data))
                    except Exception as e:
                        print(f"Erro na linha {i}: {str(e)}. Prosseguindo.")
                        continue
            if not herois:
                raise ValueError("Sem registros validos no input")
            return metodoSort, ordem, campos, herois
    except FileNotFoundError:
        print(f"Erro: arquivo '{filename}' nao encontrado")
        sys.exit(1)
    except ValueError as e:
        print(f"Erro: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"Erro: {str(e)}")
        sys.exit(1)

#escreve tudo pronto no output
def escreveOutput(filename, campos, herois):
    try:
        with open(filename, 'w') as f:
            f.write('|'.join(campos) + '\n')
            for hero in herois:
                f.write(hero.to_string() + '\n')
    except Exception as e:
        print(f"Error writing to output file: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py input_file output_file")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    #primeiro le o input
    metodoSort, ordem, campos, herois = leInput(input_file)
    
    #depois ordena
    if metodoSort == 'I':
        sorted_herois = insertion_sort(herois, ordem)
    elif metodoSort == 'M':
        sorted_herois = merge_sort(herois, ordem)
    elif metodoSort == 'Q':
        sorted_herois = quick_sort(herois, ordem)
    elif metodoSort == 'H':
        sorted_herois = heap_sort(herois, ordem)
    
    #e por ultimo escreve
    escreveOutput(output_file, campos, sorted_herois)