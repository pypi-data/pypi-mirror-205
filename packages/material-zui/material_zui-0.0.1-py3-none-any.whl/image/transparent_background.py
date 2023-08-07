from rembg import remove

input_path = 'static/img/dog 1.jpg'
output_path = 'static/img/upscale/output.png'

with open(input_path, 'rb') as i:
    with open(output_path, 'wb') as o:
        input = i.read()
        output = remove(input)
        o.write(output)  # type: ignore
