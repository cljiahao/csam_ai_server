# def create_txt_csv(path: str, table_id: str, dic: dict):
#     """Write txt with a specified file name to send to PRASS."""

#     file_name = (
#         f"{table_id}_{dt.now().strftime('%d%m%y')}_{dt.now().strftime('%H%M%S')}.txt"
#     )
#     file_path = os.path.join(path, file_name)

#     write_text(file_path, dic, "|")
