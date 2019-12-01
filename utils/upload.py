from utils.authenticate import get_drive
from utils.folders import get_default_folders


async def to_google_drive(user_id, file_path, sent_message):
    drive = get_drive(user_id)
    if not drive:
        # TODO: 允许重试
        await sent_message.edit('上传失败。请发送 /authenticate 授权 Google Drive 后重试。')
        return False

    file = drive.CreateFile()
    file['title'] = file_path.split('/')[-1]
    folders = get_default_folders(user_id)
    if folders:
        file['parents'] = [{'id': x} for x in folders]
    file.SetContentFile(file_path)
    await sent_message.edit('正在上传至 Google Drive。通常情况下 1GB 文件需要 1min 左右，如果在超出预估时间 5 倍后您依然未收到成功或失败的提醒请联系管理员。')
    try:
        file.Upload()
    except Exception as e:
        # TODO: 允许重试
        await sent_message.edit('上传失败。\n\n' + str(e))
        return

    if folders:
        await sent_message.edit(f"文件`{file['title']}`上传完成，已经存储至您设置的默认文件夹。\n\n[点此查看此文件]({file['alternateLink']})")
    else:
        await sent_message.edit(f"文件`{file['title']}`上传完成，已经存储至您网盘的根目录。\n\n[点此查看此文件]({file['alternateLink']})")
    # TODO: 删除上传完成后的文件
    # TODO: 重命名
