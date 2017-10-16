import ssl
import pika

conn_params = pika.ConnectionParameters(
                        host='192.168.0.10',
                        port=5678,
                        ssl=True,
                        ssl_options=dict(
                            ssl_version=ssl.PROTOCOL_TLSv1_2,
                            ca_certs="/home/healem/security/ca_certificate.pem",
                            keyfile="/home/healem/security/client_key.pem",
                            certfile="/home/healem/security/client_certificate.pem",
                            cert_reqs=ssl.CERT_REQUIRED))

conn = pika.BlockingConnection(conn_params)
channel = conn.channel()

channel.exchange_declare(exchange='topic_logs',
                         exchange_type='topic')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

binding_key = 'anonymous.info'

channel.queue_bind(exchange='topic_logs',
                   queue=queue_name,
                   routing_key=binding_key)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()