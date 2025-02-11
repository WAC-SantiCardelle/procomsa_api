import os
from datetime import datetime

def generate_txt(order):
    """
    Función para generar el archivo TXT con los datos del pedido.
    Args:
        order: Instancia del modelo OrderInfo
    Returns:
        bool: True si el archivo se generó correctamente
    Raises:
        Exception: Si hay algún error durante la generación del archivo
    """
    try:
        # Obtener los datos actualizados del pedido
        order_data = {
            'order_number': order.order_number,
            'order_date': order.order_date,
            'client_name': order.client_name,
            'cif': order.cif,
            'shipping_address': order.shipping_address,
            'status': order.status.status_name if order.status else 'Sin estado',
            'lines': []
        }

        # Obtener las líneas del pedido
        for line in order.lines.all():
            line_data = {
                'product_code': line.product_code,
                'quantity': line.quantity,
                'description': line.description
            }
            order_data['lines'].append(line_data)

        # Generar el nombre del archivo
        filename = f"pedido_{order.order_number}_{order.order_date.strftime('%Y%m%d')}.txt"
        
        # Crear el contenido del archivo
        content = [
            f"Número de Pedido: {order_data['order_number']}",
            f"Fecha: {order_data['order_date']}",
            f"Cliente: {order_data['client_name']}",
            f"CIF: {order_data['cif']}",
            f"Dirección de Envío: {order_data['shipping_address']}",
            f"Estado: {order_data['status']}",
            "\nLíneas de Pedido:",
            "----------------"
        ]

        for line in order_data['lines']:
            content.append(
                f"Producto: {line['product_code']} - "
                f"Cantidad: {line['quantity']} - "
                f"Descripción: {line['description']}"
            )

        # Escribir el archivo
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        txt_dir = os.path.join(base_dir, 'generated_txt')
        
        # Crear el directorio si no existe
        os.makedirs(txt_dir, exist_ok=True)
        
        file_path = os.path.join(txt_dir, filename)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content))

        return True

    except Exception as e:
        raise Exception(f"Error al generar el archivo TXT: {str(e)}")