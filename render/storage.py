import boto3
import logging
import os

from botocore.exceptions import ClientError
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible

from django.db import models



def get_client():
    """Initialize a session using DigitalOcean Spaces."""
    session = boto3.session.Session()
    spaces_region = os.environ.get("AWS_S3_REGION_NAME")
    spaces_endpoint = "https://nyc3.digitaloceanspaces.com"
    spaces_access_key = os.environ.get("AWS_ACCESS_KEY_ID")
    spaces_password = os.environ.get("AWS_SECRET_ACCESS_KEY")

    return session.client(
        "s3",
        region_name=spaces_region,
        endpoint_url=spaces_endpoint,
        aws_access_key_id=spaces_access_key,
        aws_secret_access_key=spaces_password,
    )


@deconstructible
class SpacesStorage(Storage):

    bucket = "jonathangreenstudios"

    def _save(self, name, content):

        """Save the image to a DigitalOcean Space"""
        client = get_client()
        try:
            client.upload_fileobj(
                Fileobj=content,
                Bucket=self.bucket,
                Key=name,
                ExtraArgs={"ACL": "public-read", "ContentType": content.content_type},
            )
        except ClientError as e:
            logging.error(e)

        print("NAME url func - ", self.url(name))
        return self.url(name)

    def delete(self, name):
        """Deletes image files on `post_delete`"""
        print("spaces-delete: %s" % name)
        client = get_client()

        try:
            client.delete_object(Bucket=self.bucket, Key=name)
        except ClientError as e:
            logging.error(e)

    def exists(self, name):
        """Check if the image name already exists in the Space"""
        client = get_client()

        try:
            client.get_object(Bucket=self.bucket, Key=name)
        except ClientError as e:
            logging.error(e)
            return False

        return True

    # def url(self, name):
    #     """ Return the URL to access the image on the CDN """
    #     return "https://jonathangreenstudios.nyc3.digitaloceanspaces.com/images/%s" % name

    def url(self, name):
        """Return the URL to access the image on the CDN"""
        return "https://jonathangreenstudios.nyc3.digitaloceanspaces.com/%s" % name


class ImageField(models.ImageField):
    def save_form_data(self, instance, data):
        if data is not None:
            file = getattr(instance, self.attname)

            # delete the image from the DigitalOcean space
            # if the "clear" checkbox was checked
            if file.name != "" and data is False:
                file.delete(save=False)

        super(models.ImageField, self).save_form_data(instance, data)
