from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from account.models import Credential
from .models import User, Link, Experience, Education, Skill, Graphic, Topic
from django.core import serializers
from django.shortcuts import get_object_or_404

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
                Link.objects.create(user=user, **link_data)

            # Crie as experiências
            for exp_data in data['experience']:
                Experience.objects.create(user=user, **exp_data)

            # Crie as educações
            for edu_data in data['education']:
                Education.objects.create(user=user, **edu_data)

            # Crie as habilidades
            for skill_name in data['skills']:
                Skill.objects.create(user=user, name=skill_name)

            # Crie os tópicos personalizados
            for custom_data in data['Custom']:
                if custom_data['topicType']['type'] == 'graphic':
                    Graphic.objects.create(
                        user=user,
                        title=custom_data['title'],
                        description=custom_data['description'],
                        percentage=custom_data['topicType']['percentage'],
                        color=custom_data['topicType']['color']
                    )
                elif custom_data['topicType']['type'] == 'topics':
                    Topic.objects.create(
                        user=user,
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
    if request.method == 'PUT':
        try:
            data = json.loads(request.body.decode('utf-8'))
            print(f'data: {data}')

            credential_id = data.get('id')
            print(f'credential_id: {credential_id}')

            user_data = data['user']
            print(f'user_data: {user_data}')

            # Obtenha o usuário existente
            user = User.objects.get(credential_id=credential_id)
            print(f'user: {user}')

            # Atualize os campos do usuário
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
            print('testeeeee')

            # Recuperar os IDs das entradas relacionadas
            #link_query = Link.objects.filter(user=user)
            #print(f'link_query: {link_query}')
            #link_ids = list(link_query.values_list('id', flat=True))
            #print(f'link_ids: {link_ids}')
            link_query = Link.objects.filter(user=user)
            link_ids = [link.id for link in link_query]
            print(f'link_ids: {link_ids}')
            
            experience_query = Experience.objects.filter(user=user)
            experience_ids = [exp.id for exp in experience_query]
            print(f'experience_ids: {experience_ids}')

            education_query = Education.objects.filter(user=user)
            education_ids = [edu.id for edu in education_query]
            print(f'education_ids: {education_ids}')

            skill_query = Skill.objects.filter(user=user)
            skill_ids = [skill.id for skill in skill_query]
            print(f'skill_ids: {skill_ids}')

            graphic_query = Graphic.objects.filter(user=user)
            graphic_ids = [graphic.id for graphic in graphic_query]
            print(f'graphic_ids: {graphic_ids}')

            topic_query = Topic.objects.filter(user=user)
            topic_ids = [topic.id for topic in topic_query]
            print(f'topic_ids: {topic_ids}')
            
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
                    Experience.objects.create(user=user, **exp_data)

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
                    Link.objects.create(user=user, **link_data)
            
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
                    Education.objects.create(user=user, **edu_data)

            # Atualize as habilidades
            for index, skill_data in enumerate(data['skills']):
                skill_id = skill_ids[index] if index < len(skill_ids) else None
                if skill_id:
                    print(f'skill_id: {skill_id}')
                    skill = Skill.objects.get(pk=skill_id)
                    skill.name = skill_data
                    skill.save()
                else:
                    Skill.objects.create(user=user, name=skill_data)

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
                            user=user,
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
                            user=user,
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
    if request.method == 'DELETE':
        try:
            data = json.loads(request.body.decode('utf-8'))
            credential_id = data.get('id')

            # Obtenha o usuário existente
            user = User.objects.get(credential_id=credential_id)
            
            # Exclui todas as entradas relacionadas ao usuário em todas as tabelas
            Link.objects.filter(user=user).delete()
            Experience.objects.filter(user=user).delete()
            Education.objects.filter(user=user).delete()
            Skill.objects.filter(user=user).delete()
            Graphic.objects.filter(user=user).delete()
            Topic.objects.filter(user=user).delete()
            
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
    if request.method == 'GET':

        try:        

            data = json.loads(request.body.decode('utf-8'))
            credential_id = data.get('id')
            
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
                    "id": str(user.pk),  # Chave do currículo é o ID do usuário
                    "key": str(user.key)
                }

                print('-------- TESTE -----------')

                # Verifica se o usuário tem uma chave estrangeira específica
                if user.credential_id == credential_id:
                    my_cvs.append(cv_data)
                else:
                    cvs.append(cv_data)

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
        
    return JsonResponse({'error': 'Lista não disponivel'}, status=405)

@csrf_exempt
def accessLevel(request):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body.decode('utf-8'))
            credential_id = data.get('id')
            access_level = data.get('accessLevel')

            # Obtenha o usuário existente
            user = User.objects.get(credential_id=credential_id)            

            user = User.objects.get(credential_id=credential_id)
            user.access_level = access_level
            user.save()

            return JsonResponse({'message': 'Sucesso ao atualizar o tipo de acesso'})
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def published(request):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body.decode('utf-8'))
            credential_id = data.get('id')
            published = data.get('published')

            # Obtenha o usuário existente
            user = User.objects.get(credential_id=credential_id)   
            user.published = published
            user.save()

            return JsonResponse({'message': 'Sucesso ao atualizar o status de publicação'})
        except User.DoesNotExist:
            return JsonResponse({'error': 'Usuário não encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Metodo não permitido'}, status=405)
    
@csrf_exempt
def profile(request):
    if request.method == 'GET':

        try:
            data = json.loads(request.body.decode('utf-8'))
            credential_id = data.get('id')

            # Obtenha o usuário existente
            user = User.objects.get(credential_id=credential_id)
            user_data = {
                "name": user.name,
                "title": user.title,
                "email": user.email,
                "phone": user.phone,
                "location": user.location,
                "avatar": user.avatar,
                "gender": user.gender,
                "pronoun": user.pronoun,
                "description": user.description,
                "accessLevel": user.access_level,
                "published": user.published,
                "created_at": user.created_at,
                "updated_at": user.updated_at,
                "key": user.key,
                "id": user.id
            }

            links = Link.objects.filter(user=user)
            links_data = [{"name": link.name, "url": link.url} for link in links]

            experiences = Experience.objects.filter(user=user)
            experiences_data = [{
                "company": experience.company,
                "position": experience.position,
                "period": experience.period,
                "description": experience.description
            } for experience in experiences]

            educations = Education.objects.filter(user=user)
            educations_data = [{
                "institution": education.institution,
                "course": education.course,
                "period": education.period,
                "description": education.description
            } for education in educations]

            skills = Skill.objects.filter(user=user)
            skills_data = [skill.name for skill in skills]

            custom_data = []
            graphics = Graphic.objects.filter(user=user)
            for graphic in graphics:
                custom_data.append({
                    "title": graphic.title,
                    "description": graphic.description,
                    "topicType": {
                        "type": graphic.type,
                        "description": graphic.description,
                        "percentage": graphic.percentage,
                        "color": graphic.color
                    }
                })

            topics = Topic.objects.filter(user=user)
            for topic in topics:
                custom_data.append({
                    "title": topic.title,
                    "description": topic.description,
                    "topicType": {
                        "type": topic.type,
                        "topics": topic.topics
                    }
                })

            response_data = {
                "user": user_data,
                "links": links_data,
                "experience": experiences_data,
                "education": educations_data,
                "skills": skills_data,
                "Custom": custom_data
            }

            return JsonResponse(response_data)
        except User.DoesNotExist:
            return JsonResponse({"error": "Only POST requests are allowed."}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    else:
        return JsonResponse({'error': 'Perfil não existe.'}, status=405)
