from state import *
import asyncio

urls = [
    ('https://canary.discord.com/api/webhooks/1299721567730667560/KSuMVIYEfJGnc1kzk8djNPJ5fqIMJNNonedN-hcpaKxrWgq2S1hASW7h-7UYrIog7IIw', True),# Transcendent
    ('https://discordapp.com/api/webhooks/1304361125562941491/ZZftwokaYbFe-KeI_AC7vTmjn1VX-StmMD4aPstZSGFFRgzH8xMOqgohpCO1OJyAQbAm', False) # Chimera Team
]
webhook_state(urls[:1])
