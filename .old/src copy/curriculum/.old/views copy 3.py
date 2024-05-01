from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from account.models import Credential
from .models import User, Link, Experience, Education, Skill, Graphic, Topic

@csrf_exempt
def create(request):
    if request.method == 'POST':
        try:
                        
            data = json.loads(request.body.decode('utf-8'))
            print(data)

            credential_id = data.get('id')
            print(f'credential_id: {credential_id}')

            # Inserir dados do usuário
            user_data = data['user']
            user = User.objects.create(
                name=user_data['name'],
                title=user_data['title'],
                email=user_data['email'],
                phone=user_data['phone'],
                location=user_data['location'],
                avatar=user_data['avatar'],
                gender=user_data['gender'],
                pronoun=user_data['pronoun'],
                description=user_data['description'],
                credential_id=credential_id
    )

            # Crie os links
            for link_data in data['links']:
                Link.objects.create(credential_id=credential_id, **link_data)

            # Crie as experiências
            for exp_data in data['experience']:
                Experience.objects.create(credential_id=credential_id, **exp_data)

            # Crie as educações
            for edu_data in data['education']:
                Education.objects.create(credential_id=credential_id, **edu_data)

            # Crie as habilidades
            for skill_name in data['skills']:
                Skill.objects.create(credential_id=credential_id, name=skill_name)

            # Crie os tópicos personalizados
            for custom_data in data['Custom']:
                if custom_data['topicType']['type'] == 'graphic':
                    Graphic.objects.create(
                        credential_id=credential_id,
                        title=custom_data['title'],
                        description=custom_data['description'],
                        percentage=custom_data['topicType']['percentage'],
                        color=custom_data['topicType']['color']
                    )
                elif custom_data['topicType']['type'] == 'topics':
                    Topic.objects.create(
                        credential_id=credential_id,
                        title=custom_data['title'],
                        description=custom_data['description'],
                        topics=custom_data['topicType']['topics']
                    )

            # Retorne uma resposta de sucesso
            return JsonResponse({'message': 'Criado com sucesso'})

        except Exception as e:
            # Em caso de qualquer exceção, retorne uma resposta de erro
            return JsonResponse({'error': str(e)}, status=500)

    # Se não for um request POST, retorne um erro de método não permitido
    return JsonResponse({'error': 'Método não permitido'}, status=405)

@csrf_exempt
def update(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            print(data)

            credential_id = data.get('id')

            # Recuperar os IDs das entradas relacionadas
            user_ids = list(User.objects.filter(credential_id=credential_id).values_list('id', flat=True))
            link_ids = list(Link.objects.filter(credential_id=credential_id).values_list('id', flat=True))
            experience_ids = list(Experience.objects.filter(credential_id=credential_id).values_list('id', flat=True))
            education_ids = list(Education.objects.filter(credential_id=credential_id).values_list('id', flat=True))
            skill_ids = list(Skill.objects.filter(credential_id=credential_id).values_list('id', flat=True))
            graphic_ids = list(Graphic.objects.filter(credential_id=credential_id).values_list('id', flat=True))
            topic_ids = list(Topic.objects.filter(credential_id=credential_id).values_list('id', flat=True))

            # Atualize os links
            for user_data in data['user']:
                user_id = user_ids.pop(0) if user_ids else None
                if user_id:
                    print(f'link_id: {link_id}')
                    user = User.objects.get(pk=credential_id)
                    user.name = user_data['name']
                    user.title = user_data['title']
                    user.email = user_data['email']
                    user.phone = user_data['phone']
                    user.location = user_data['location']
                    user.avatar = user_data['avatar']
                    user.gender = user_data['gender']
                    user.pronoun = user_data['pronoun']
                    user.description = user_data['description']
                    user.save()            

            # Atualize os links
            for link_data in data['links']:
                link_id = link_ids.pop(0) if link_ids else None
                if link_id:
                    print(f'link_id: {link_id}')
                    link = Link.objects.get(pk=link_id)
                    link.name = link_data['name']
                    link.url = link_data['url']
                    link.save()
                else:
                    Link.objects.create(credential_id=credential_id, **link_data)
            
            # Atualize as experiências
            for exp_data in data['experience']:
                exp_id = experience_ids.pop(0) if experience_ids else None
                if exp_id:
                    print(f'exp_id: {exp_id}')
                    experience = Experience.objects.get(pk=exp_id)
                    experience.company = exp_data['company']
                    experience.position = exp_data['position']
                    experience.period = exp_data['period']
                    experience.description = exp_data['description']
                    experience.save()
                else:
                    Experience.objects.create(credential_id=credential_id, **exp_data)
            
            # Atualize as educações
            for edu_data in data['education']:
                edu_id = education_ids.pop(0) if education_ids else None
                if edu_id:
                    print(f'edu_id: {edu_id}')
                    education = Education.objects.get(pk=edu_id)
                    education.institution = edu_data['institution']
                    education.course = edu_data['course']
                    education.period = edu_data['period']
                    education.description = edu_data['description']
                    education.save()
                else:
                    Education.objects.create(credential_id=credential_id, **edu_data)

            # Atualize as habilidades
            for index, skill_data in enumerate(data['skills']):
                skill_id = skill_ids[index] if index < len(skill_ids) else None
                if skill_id:
                    print(f'skill_id: {skill_id}')
                    skill = Skill.objects.get(pk=skill_id)
                    skill.name = skill_data
                    skill.save()
                else:
                    Skill.objects.create(credential_id=credential_id, name=skill_data)

            # Atualize os gráficos e tópicos personalizados
            for custom_data in data['Custom']:
                custom_id = None
                if custom_data['topicType']['type'] == 'graphic':
                    custom_id = graphic_ids.pop(0) if graphic_ids else None
                    if custom_id:
                        print(f'custom_id: {custom_id}')
                        graphic = Graphic.objects.get(pk=custom_id)
                        graphic.title = custom_data['title']
                        graphic.description = custom_data['description']
                        graphic.percentage = custom_data['topicType']['percentage']
                        graphic.color = custom_data['topicType']['color']
                        graphic.save()
                    else:
                        Graphic.objects.create(
                            credential_id=credential_id,
                            title=custom_data['title'],
                            description=custom_data['description'],
                            percentage=custom_data['topicType']['percentage'],
                            color=custom_data['topicType']['color']
                        )
                elif custom_data['topicType']['type'] == 'topics':
                    custom_id = topic_ids.pop(0) if topic_ids else None
                    if custom_id:
                        print(f'custom_id: {custom_id}')
                        topic = Topic.objects.get(pk=custom_id)
                        topic.title = custom_data['title']
                        topic.description = custom_data['description']
                        topic.topics = custom_data['topicType']['topics']
                        topic.save()
                    else:
                        Topic.objects.create(
                            credential_id=credential_id,
                            title=custom_data['title'],
                            description=custom_data['description'],
                            topics=custom_data['topicType']['topics']
                        )

            # Retorne uma resposta de sucesso
            return JsonResponse({'message': 'Atualizado com sucesso'})

        except User.DoesNotExist:
            return JsonResponse({'error': 'Usuário não encontrado'}, status=404)
        except Exception as e:
            # Em caso de qualquer exceção, retorne uma resposta de erro
            return JsonResponse({'error': str(e)}, status=500)

    # Se não for um request POST, retorne um erro de método não permitido
    return JsonResponse({'error': 'Método não permitido'}, status=405)

@csrf_exempt
def delete(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))

            credential_id = data.get('id')

            # Obtenha o usuário existente
            user = User.objects.get(pk=credential_id)
            
            # Exclui todas as entradas relacionadas ao usuário em todas as tabelas
            Link.objects.filter(credential_id=credential_id).delete()
            Experience.objects.filter(credential_id=credential_id).delete()
            Education.objects.filter(credential_id=credential_id).delete()
            Skill.objects.filter(credential_id=credential_id).delete()
            Graphic.objects.filter(credential_id=credential_id).delete()
            Topic.objects.filter(credential_id=credential_id).delete()
            
            # Exclui o usuário em si
            user.delete()
            
            return JsonResponse({'message': 'Usuário excluído com sucesso'})

        except User.DoesNotExist:
            return JsonResponse({'error': 'Usuário não encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método não permitido'}, status=405)

@csrf_exempt
def list(request):
    try:
        # Consulta todos os usuários (currículos)
        users = User.objects.all()

        # Lista para armazenar os currículos formatados
        cvs = []
        my_cvs = []

        # Itera sobre os usuários e formata os dados
        for user in users:
            cv_data = {
                "name": user.name,
                "title": user.title,
                "key": str(user.pk)  # Chave do currículo é o ID do usuário
            }

            # Adiciona o currículo à lista correspondente
            if user.status:
                cvs.append(cv_data)
            else:
                my_cvs.append(cv_data)

        # Cria o objeto de resposta com os currículos formatados
        response_data = {
            "cvs": cvs,
            "myCvs": my_cvs
        }

        # Retorna a resposta como JSON
        return JsonResponse(response_data)

    except Exception as e:
        # Em caso de qualquer exceção, retorne uma resposta de erro
        return JsonResponse({'error': str(e)}, status=500)
