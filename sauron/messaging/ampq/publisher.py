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

routing_key = 'anonymous.info'
message = 'Hello World!'
channel.basic_publish(exchange='topic_logs',
                      routing_key=routing_key,
                      body=message)
print(" [x] Sent %r:%r" % (routing_key, message))
conn.close()