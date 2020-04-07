def clip(text, max_len=80):
  """在 maxlen 前面或后面的第一个空格处截断文本
  """
  end = None
  if len(text) > max_len:
    space_before = text.rfind(' ', 0, max_len)
    if space_before >= 0:
      end = space_before
    else:
      sapce_after = text.rfind(' ', max_len)
      if space_after >= 0:
        end = space_after
  if end is None:  # 没有找到空格
    end = len(text)
  return text[:end].rstrip()