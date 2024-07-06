import os
import tkinter as tk
from tkinter import filedialog, messagebox
import datetime

def select_folder():
    folder_selected = filedialog.askdirectory()
    folder_path.set(folder_selected)

def replace_text():
    folder = folder_path.get()
    old_str = old_string.get()
    new_str = new_string.get()
    
    if not folder or not old_str or not new_str:
        messagebox.showerror("エラー", "すべてのフィールドを入力してください")
        return

    log_entries = []
    errors_occurred = False

    try:
        for root, dirs, files in os.walk(folder):
            for filename in files:
                if filename.endswith('.pl3'):
                    file_path = os.path.join(root, filename)
                    
                    try:
                        with open(file_path, 'rb') as file:
                            binary_content = file.read()
                        
                        binary_str = binary_content.decode('ISO-8859-1')
                        if old_str in binary_str:
                            modified_str = binary_str.replace(old_str, new_str)
                            modified_binary_content = modified_str.encode('ISO-8859-1')
                        
                            with open(file_path, 'wb') as file:
                                file.write(modified_binary_content)
                            
                            log_entries.append(f"置換成功: {file_path}")
                        else:
                            log_entries.append(f"文字列が見つかりませんでした: {file_path}")
                    except Exception as e:
                        log_entries.append(f"置換失敗: {file_path}, エラー: {str(e)}")
                        errors_occurred = True

        log_path = os.path.join(folder, f"replace_log_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
        try:
            with open(log_path, 'w', encoding='utf-8') as log_file:
                log_file.write('\n'.join(log_entries))
            
            if errors_occurred:
                messagebox.showwarning("警告", f"処理中にエラーが発生しました。詳細はログファイルを確認してください: {log_path}")
            else:
                messagebox.showinfo("完了", f"フォルダ内のすべての .pl3 ファイルで置換処理が完了しました。ログファイル: {log_path}")
        except Exception as e:
            messagebox.showerror("ログファイルエラー", f"ログファイルの作成中にエラーが発生しました: {str(e)}")

    except Exception as e:
        messagebox.showerror("フォルダエラー", f"フォルダの処理中にエラーが発生しました: {str(e)}")

app = tk.Tk()
app.title("BinaryReplaceTool")

folder_path = tk.StringVar()
old_string = tk.StringVar()
new_string = tk.StringVar()

tk.Label(app, text="フォルダを選択:").grid(row=0, column=0, padx=10, pady=10)
tk.Entry(app, textvariable=folder_path, width=50).grid(row=0, column=1, padx=10, pady=10)
tk.Button(app, text="フォルダを選択", command=select_folder).grid(row=0, column=2, padx=10, pady=10)

tk.Label(app, text="置換前の文字列:").grid(row=1, column=0, padx=10, pady=10)
tk.Entry(app, textvariable=old_string, width=50).grid(row=1, column=1, padx=10, pady=10)

tk.Label(app, text="置換後の文字列:").grid(row=2, column=0, padx=10, pady=10)
tk.Entry(app, textvariable=new_string, width=50).grid(row=2, column=1, padx=10, pady=10)

tk.Button(app, text="置換を実行", command=replace_text).grid(row=3, columnspan=3, padx=10, pady=10)

app.mainloop()
