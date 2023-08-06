# coding=utf-8
# Copyright 2018-2022 EVA
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from typing import List

from eva.catalog.models.udf_metadata_catalog import (
    UdfMetadataCatalog,
    UdfMetadataCatalogEntry,
)
from eva.catalog.services.base_service import BaseService
from eva.utils.errors import CatalogError
from eva.utils.logging_manager import logger


class UdfMetadataCatalogService(BaseService):
    def __init__(self):
        super().__init__(UdfMetadataCatalog)

    def insert_entries(self, entries: List[UdfMetadataCatalogEntry]):
        try:
            for entry in entries:
                metadata_obj = UdfMetadataCatalog(
                    key=entry.key, value=entry.value, udf_id=entry.udf_id
                )
                metadata_obj.save()
        except Exception as e:
            logger.exception(
                f"Failed to insert entry {entry} into udf metadata catalog with exception {str(e)}"
            )
            raise CatalogError(e)

    def get_entries_by_udf_id(self, udf_id: int) -> List[UdfMetadataCatalogEntry]:
        try:
            result = self.model.query.filter(
                self.model._udf_id == udf_id,
            ).all()
            return [obj.as_dataclass() for obj in result]
        except Exception as e:
            error = f"Getting metadata entries for UDF id {udf_id} raised {e}"
            logger.error(error)
            raise CatalogError(error)
