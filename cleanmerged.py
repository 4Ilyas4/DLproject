import pandas as pd

def drop_duplicate_columns_smaller(df, sample_size=10000, threshold=0.95):

    duplicate_cols = set()
    cols = list(df.columns)
    non_null_counts = df.count()

    for i in range(len(cols)):
        if cols[i] in duplicate_cols:
            continue
        for j in range(i + 1, len(cols)):
            if cols[j] in duplicate_cols:
                continue

            series_i = df[cols[i]].head(sample_size)
            series_j = df[cols[j]].head(sample_size)

            series_i_filled = series_i.fillna('__NA__')
            series_j_filled = series_j.fillna('__NA__')

            total = min(len(series_i_filled), len(series_j_filled))
            if total == 0:
                continue

            match_count = (series_i_filled == series_j_filled).sum()
            percent_match = match_count / total

            if percent_match >= threshold:
                if non_null_counts[cols[i]] <= non_null_counts[cols[j]]:
                    duplicate_cols.add(cols[i])

                    break  
                else:
                    duplicate_cols.add(cols[j])
                    
    return df.drop(columns=list(duplicate_cols))

# Загружаем df2 полностью (предполагаем, что он меньше)
df2 = pd.read_csv("C:/Users/user/Desktop/CatCTCPartM.csv", dtype=str, low_memory=True)
# Очистка ключа в df2
df2["PartID"] = df2["PartID"].str.strip()

# Путь к файлу для сохранения результата
result_file = "C:/Users/user/Desktop/Merged_by_PartID_chunked.csv"

# Задаём размер чанка (например, 100 000 строк за раз)
chunksize = 100000

# Флаг для записи заголовка только в первый раз
first_chunk = True

# Читаем df1 по частям и объединяем каждую часть с df2
for chunk in pd.read_csv("C:/Users/user/Desktop/HotspotGSPPLine.csv", 
                          dtype=str, low_memory=True, chunksize=chunksize):
    # Очистка столбца PartID в текущем чанке
    chunk["PartID"] = chunk["PartID"].str.strip()
    
    # Выполняем объединение по PartID (inner join)
    merged_chunk = chunk.merge(df2, on="PartID", how="inner")
    
    # Записываем результат на диск: для первого чанка с заголовком, для остальных без
    if first_chunk:
        merged_chunk.to_csv(result_file, index=False, mode="w")
        first_chunk = False
    else:
        merged_chunk.to_csv(result_file, index=False, mode="a", header=False)
    
    print(f"Обработан чанк размером {chunk.shape}, объединено строк: {merged_chunk.shape[0]}")

print("Объединение завершено!")
