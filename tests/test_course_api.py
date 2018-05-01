# from django.contrib.auth.models import User
# from django.core.urlresolvers import reverse
# from rest_framework import status
# from rest_framework.test import APITestCase
#
# # from courses.serializers import CourseSerializer, CourseDetailSerializer
# from courses.models import Course
#
#
# class CreateCourseTest(APITestCase):
#     def setUp(self):
#         self.data = {'name': 'Bunker Hills', 'description': 'South'}
#
#     def test_authenticated_user_can_create_course(self):
#         self.superuser = User.objects.create_superuser('john', 'john@snow.com', 'johnpassword')
#         self.client.login(username='john', password='johnpassword')
#         response = self.client.post(reverse('course-list'), self.data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#
#     def test_anonymous_user_cannot_create_course(self):
#         response = self.client.post(reverse('course-list'), self.data)
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#
#
# class ReadCourseTest(APITestCase):
#
#     fixtures = ['courses.json', 'holes.json']
#
#     def test_can_read_course_list(self):
#         response = self.client.get(reverse('course-list'))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertIsNotNone(response.data[2])
#
#     def test_can_read_course_detail(self):
#         response = self.client.get(reverse('course-detail', args=[1]))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_return_404_for_missing_course_detail(self):
#         response = self.client.get(reverse('course-detail', args=[4]))
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#
#
# # class UpdateCourseTest(APITestCase):
# #     def setUp(self):
# #         self.superuser = User.objects.create_superuser('john', 'john@snow.com', 'johnpassword')
# #         self.client.login(username='john', password='johnpassword')
# #         self.user = User.objects.create(username="mike", first_name="Tyson")
# #         self.data = UserSerializer(self.user).data
# #         self.data.update({'first_name': 'Changed'})
# #
# #     def test_can_update_user(self):
# #         response = self.client.put(reverse('user-detail', args=[self.user.id]), self.data)
# #         self.assertEqual(response.status_code, status.HTTP_200_OK)
# #
# #
# # class DeleteCourseTest(APITestCase):
# #     def setUp(self):
# #         self.superuser = User.objects.create_superuser('john', 'john@snow.com', 'johnpassword')
# #         self.client.login(username='john', password='johnpassword')
# #         self.user = User.objects.create(username="mikey")
# #
# #     def test_can_delete_user(self):
# #         response = self.client.delete(reverse('user-detail', args=[self.user.id]))
# #         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)