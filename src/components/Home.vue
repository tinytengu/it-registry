<template>
    <div class="container d-flex flex-column align-items-center justify-content-center gap-4">
        <h2>Поиск организации в реестре</h2>
        <div class="input-group d-flex flex-column flex-sm-row gap-3 gap-sm-0">
            <!-- Search fields (ИНН, ...) -->
            <button id="fieldsBtn" class="btn btn-outline-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown">
                {{ search.fields[search.fieldIdx] }}
            </button>
            <ul class="dropdown-menu">
                <li>
                    <a class="dropdown-item" href="#" v-for="(field, idx) in search.fields" :key="field" @click="search.fieldIdx = idx">
                        {{ field }}
                    </a>
                </li>
            </ul>
            <!-- Search filter type -->
            <button class="btn btn-outline-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown">
                {{ search.filters[search.filterIdx] }}
            </button>
            <ul class="dropdown-menu">
                <li>
                    <a class="dropdown-item" href="#" v-for="(filter, idx) in search.filters" :key="filter" @click="search.filterIdx = idx">
                        {{ filter }}
                    </a>
                </li>
            </ul>
            <!-- Search input -->
            <input type="text" class="form-control w-auto" v-model="search.value" placeholder="Значение">
            <!-- Search button -->
            <a href="#" class="btn btn-primary px-3" @click="searchOrganization">Поиск</a>
        </div>

        <div class="modal fade" id="infoModal" tabindex="-1">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Организация</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <p v-for="(field, idx) in search.fields" :key="field">
                        <b>{{ field }}:</b> {{ organization[idx] }}
                    </p>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
                </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { Modal } from "bootstrap";
import axios from "axios";
import { csvStringToArray } from "../utils/csv";

export default {
    data() {
        return {
            search: {
                fields: [
                    "Регистрационный номер",
                    "Дата внесения записи",
                    "Наименование организации",
                    "Регистрационный номер по ЕГРЮЛ",
                    "Актуальный регистрационный номер по ЕГРЮЛ",
                    "ИНН",
                    "Дата и номер решения об аккредитации",
                    "Сведения об изменениях",
                    "Место регистрации организации"
                ],
                fieldIdx: 0,
                filters: [
                    "содержит",
                    "равен",
                    "начинается с",
                    "заканчивается на",
                ],
                filterIdx: 0
            },
            organizations: [],
            organization: [],
            value: ""
        }
    },
    methods: {
        searchOrganization() {
            this.organization = [];
            let found = false;

            const patterns = [
                `${this.search.value}`,
                `^${this.search.value}$`,
                `^${this.search.value}`,
                `${this.search.value}$`
            ];
            const pattern = new RegExp(patterns[this.search.filterIdx], 'i');

            for (let i = 1; i < this.organizations.length; i++) {
                if (this.organizations[i][this.search.fieldIdx].match(pattern)) {
                    this.organization = this.organizations[i];
                    found = true;
                    break;
                }
            }
            
            if (!found) {
                alert("Организация не найдена");
                return;
            }

            this.showModal();
        },
        showModal() {
            var modal = new Modal(document.getElementById('infoModal'), {});
            modal.show();
        }
    },
    mounted() {
        axios.get('https://raw.githubusercontent.com/tinytengu/it-registry/main/dump.csv')
        .then((response) => {
            this.organizations = csvStringToArray(response.data);
        })
        .catch((error) => alert(error));
    }
}
</script>

<style scoped>
#fieldsBtn {
    width: 100%;
    text-overflow: ellipsis;
    overflow: hidden;
}

@media (min-width: 576px) {
    #fieldsBtn {
        width: 10rem;
    }
}
</style>