from django.http import JsonResponse
from .models import TimeCapsule
from .IPFS import FilebaseIPFS
from .BLOCK_CHAIN import ChainContract
from django.core.exceptions import ValidationError
# from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from WORKER.utility_functions import utility_functions
client =utility_functions()

contract = ChainContract()  # Initialize the contract
ipfs = FilebaseIPFS()


def homepage(request):
    return render(request, 'index.html')

def formpage(request):
    return render(request, 'form.html')

def signuppage(request):
    return render(request, 'signup.html')


def process_secure_upload(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

    try:
        # Get the uploaded file object
        file_bytes = request.FILES.get('encrypted_file').read()
        if not file_bytes:
            raise ValidationError("No file was uploaded")
        else:
            '''
            
            storing file to ipfs to get cid 
            
            '''
        # Get form data
        unlock_time = int(request.POST.get('unlock_time'))
        email = request.POST.get('email')
        decryption_password = request.POST.get('password')
        ext = request.POST.get('file_ext')
        mime= request.POST.get('file_mime')
        # print(client.decrypt_aes256_cbc(uploaded_file, decryption_password))

        capsule_count = TimeCapsule.objects.filter(email=email).count()
        # if capsule_count >=2:
        #     return JsonResponse({'error': 'You have reached the maximum limit of 2 capsules.'}, status=400)

        # Initialize IPFS client
        cid = ipfs.upload_and_get_cid(file_bytes)  # upload file to IPFS and get CID

        if not all([unlock_time, email, decryption_password]):
            raise ValidationError("All fields (unlock_time, email, password) are required")
        print("got all data ")

        '''
        
        storing cid and to sepoliaetherium  via smart contracts 
         
         '''
        try:
            print("storing to blockchain")
            contract.store_data(cid,unlock_time)
        except Exception as e:
            print("failed to store to blockchain")
            ipfs.delete_file_by_cid(cid)
            raise ValidationError("Failed to store data on the blockchain") from e

        '''
        storing to mysql database 

        '''
        TimeCapsule.objects.create(
            email=email,
            cid=cid[-12:],
            decryption_pass = decryption_password,
            unlock_time = unlock_time,
            file_ext = ext,
            file_mime = mime
        )

        return JsonResponse("stored successfully", safe=False, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)